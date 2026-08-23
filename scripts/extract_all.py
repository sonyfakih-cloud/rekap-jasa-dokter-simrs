"""
Ekstraksi 6 file bulanan .xlsb (SIMRS) -> data_source/data_v5.json

Cara pakai:
1. Salin 6 file .xlsb bulanan (dari Google Drive folder "TENAGA MEDIS SIMRS POIN")
   ke dalam folder `data_source/` di root repo ini (sejajar dengan folder `scripts/`).
   Nama file harus persis sama seperti di FILES di bawah -- kalau nama beda,
   sesuaikan daftar FILES.
2. Jalankan dari root repo:  python3 scripts/extract_all.py
3. Hasilnya: data_source/data_v5.json (JANGAN di-commit ke git -- lihat .gitignore,
   file ini berisi data rinci per-kunjungan pasien: No RM & Nama Pasien).
4. Lanjutkan dengan: python3 scripts/build.py  (menghasilkan index.html di root repo)
"""
import pyxlsb, json, re, os, collections, html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(SCRIPT_DIR, '..', 'data_source')

FILES = [
    ('2026-01', 'TEMPLATE KSI JANUARI 2026 BASIS TARIF MURNI BARU.xlsb'),
    ('2026-02', 'TEMPLATE KSI FEBRUARI 2026 BASIS TARIF MURNI BARU.xlsb'),
    ('2026-03', 'TEMPLATE KSI MARET 2026 BASIS TARIF MURNI BARU.xlsb'),
    ('2026-04', 'TEMPLATE KSI APRIL 2026 BASIS TARIF MURNI BARU.xlsb'),
    ('2026-05', 'TEMPLATE KSI MEI 2026 BASIS TARIF MURNI BARU.xlsb'),
    ('2026-06', 'TEMPLATE KSI JUNI 2026 BASIS TARIF MURNI BARU.xlsb'),
    # Tambahkan bulan baru di sini, mis:
    # ('2026-07', 'TEMPLATE KSI JULI 2026 BASIS TARIF MURNI BARU.xlsb'),
]

def clean(v):
    if v is None:
        return ''
    if isinstance(v, str):
        # sumber data kadang berisi entity HTML (mis. "MAR&#039;ATUN") dari proses
        # export/import sebelumnya -- decode supaya tampil sbg teks asli (MAR'ATUN).
        return html.unescape(v.strip())
    return v

def num(v):
    try:
        return float(v)
    except Exception:
        return 0.0

def norm_key(s):
    return re.sub(r'\s+', ' ', str(s).strip().lower())

class Dict_:
    def __init__(self):
        self.key_to_idx = {}
        self.display = []

    def id(self, raw):
        raw = raw if raw else '(lainnya)'
        key = norm_key(raw)
        if key not in self.key_to_idx:
            self.key_to_idx[key] = len(self.display)
            self.display.append(raw)
        return self.key_to_idx[key]

    def list(self):
        return self.display

DOC = Dict_()
TIND = Dict_()
SUB = Dict_()
KSO = Dict_()
UNIT = Dict_()
OBAT = Dict_()
DATE = Dict_()
ANES = Dict_()  # dokter/petugas anestesi (kolom BB, hanya utk TINDAKAN MEDIS OPERATIF)
RM = Dict_()      # no_RM / id_pasien
PASIEN = Dict_()  # nama pasien
NOPJ = Dict_()    # no penjualan (obat)

t_group = {}  # key(tuple ints incl. anesIdx) -> [count, japel, jsarrs, operator, anestesi, team, biaya]
o_group = {}  # key(tuple ints) -> [count, qty, profit]
t_detail = []  # baris rinci per-kunjungan utk baris yg memenuhi syarat Tindakan Dilaksanakan (Unik)
o_detail = []  # baris rinci per-transaksi obat (semua baris valid, tanpa syarat tambahan)

def process_file(month_prefix, fname):
    path = os.path.join(BASE, fname)
    print(f"Processing {fname} ...", flush=True)
    wb = pyxlsb.open_workbook(path)

    n1 = 0
    with wb.get_sheet('TABEL IL ITL KRM N OB') as sheet:
        for i, row in enumerate(sheet.rows()):
            if i < 2:
                continue
            if len(row) < 31:
                continue
            cells = {c.c: c.v for c in row}
            pelaksana = clean(cells.get(15))
            if not pelaksana:
                continue
            tindakan = clean(cells.get(19)) or '(tanpa nama)'
            subklas = clean(cells.get(21))
            kso = clean(cells.get(13))
            unit = clean(cells.get(9))
            tgl_raw = clean(cells.get(2))
            tgl = str(tgl_raw)[:10] if tgl_raw else (month_prefix + '-01')
            # guard against stray dates outside this file's month (data entry errors) by keeping actual value;
            # filtering/reporting of anomalies handled separately if needed.
            japel = num(cells.get(26))
            j_sarrs = num(cells.get(27))
            operator = num(cells.get(28))
            anestesi = num(cells.get(29))
            team = num(cells.get(30))
            biaya = num(cells.get(25))

            # Kolom BB (idx 53) = "Petugas 6". Untuk baris TINDAKAN MEDIS OPERATIF
            # (operator dokter bedah/obsgyn/tulang), kolom ini berisi nama dokter/petugas
            # anestesi. Untuk subklasifikasi lain kolom ini dipakai utk keperluan berbeda
            # (petugas lain) sehingga TIDAK dianggap sbg dokter anestesi -> diabaikan (-1).
            is_operatif = subklas == 'TINDAKAN MEDIS OPERATIF'
            anes_raw = clean(cells.get(53)) if is_operatif else ''
            anes_idx = ANES.id(anes_raw) if anes_raw else -1

            key = (
                DOC.id(pelaksana), TIND.id(tindakan), SUB.id(subklas),
                KSO.id(kso), UNIT.id(unit), DATE.id(tgl), anes_idx
            )
            g = t_group.get(key)
            if g is None:
                t_group[key] = [1, japel, j_sarrs, operator, anestesi, team, biaya]
            else:
                g[0] += 1; g[1] += japel; g[2] += j_sarrs; g[3] += operator; g[4] += anestesi; g[5] += team; g[6] += biaya
            n1 += 1

            # Baris rinci per-kunjungan (No RM, Nama Pasien) -- hanya utk baris yg memenuhi
            # syarat Tindakan Dilaksanakan (Unik): japel > 0 atau operator > 0.
            if japel > 0 or operator > 0:
                no_rm = clean(cells.get(5))
                pasien = clean(cells.get(6)) or '(tanpa nama)'
                qty = num(cells.get(24))
                t_detail.append([
                    DATE.id(tgl), RM.id(no_rm), PASIEN.id(pasien), KSO.id(kso), UNIT.id(unit),
                    DOC.id(pelaksana), TIND.id(tindakan), SUB.id(subklas),
                    int(round(qty)), int(round(japel)), int(round(j_sarrs)),
                    int(round(operator)), int(round(anestesi)), int(round(team)), int(round(biaya)),
                ])

    n2 = 0
    with wb.get_sheet('TABEL KRM OB') as sheet:
        for i, row in enumerate(sheet.rows()):
            if i < 4:
                continue
            if len(row) < 22:
                continue
            cells = {c.c: c.v for c in row}
            dokter = clean(cells.get(17))
            if not dokter:
                continue
            obat = clean(cells.get(9)) or '(tanpa nama)'
            kso = clean(cells.get(7))
            unit = clean(cells.get(16))
            tgl_raw = clean(cells.get(1))
            tgl = str(tgl_raw)[:10] if tgl_raw else (month_prefix + '-01')
            qty = num(cells.get(11))
            profit_total = num(cells.get(20))

            key = (
                DOC.id(dokter), OBAT.id(obat), KSO.id(kso), UNIT.id(unit), DATE.id(tgl)
            )
            g = o_group.get(key)
            if g is None:
                o_group[key] = [1, qty, profit_total]
            else:
                g[0] += 1; g[1] += qty; g[2] += profit_total
            n2 += 1

            # Baris rinci per-transaksi obat (No Penjualan, No RM, Nama Pasien, Harga Total)
            no_penjualan = clean(cells.get(2))
            no_rm2 = clean(cells.get(3))
            pasien2 = clean(cells.get(4)) or '(tanpa nama)'
            harga_total = num(cells.get(14))
            o_detail.append([
                DATE.id(tgl), NOPJ.id(no_penjualan), RM.id(no_rm2), PASIEN.id(pasien2), KSO.id(kso),
                OBAT.id(obat), round(qty, 2), int(round(harga_total)), UNIT.id(unit), DOC.id(dokter),
            ])

    print(f"  -> tindakan rows: {n1}, obat rows: {n2}", flush=True)

for month_prefix, fname in FILES:
    process_file(month_prefix, fname)

print("Building output structures...", flush=True)

t_rows = []
for key, g in t_group.items():
    docIdx, tIdx, sIdx, kIdx, uIdx, dtIdx, anesIdx = key
    cnt, japel, jsarrs, operator, anestesi, team, biaya = g
    t_rows.append([docIdx, tIdx, sIdx, kIdx, uIdx, dtIdx, cnt,
                   int(round(japel)), int(round(jsarrs)), int(round(operator)),
                   int(round(anestesi)), int(round(team)), int(round(biaya)), anesIdx])

o_rows = []
for key, g in o_group.items():
    docIdx, oIdx, kIdx, uIdx, dtIdx = key
    cnt, qty, profit = g
    o_rows.append([docIdx, oIdx, kIdx, uIdx, dtIdx, cnt, round(qty, 2), int(round(profit))])

def is_doctor(name):
    n = name.strip().lower()
    return n.startswith('dr.') or n.startswith('dr ') or n.startswith('drg')

SPEC_FULL = {
    'Sp. A': 'Anak', 'Sp. AN': 'Anestesi', 'Sp. B': 'Bedah',
    'Sp. JP': 'Jantung & Pembuluh Darah', 'Sp. KFR': 'Kedokteran Fisik & Rehabilitasi',
    'Sp. KG': 'Konservasi Gigi', 'Sp. KJ': 'Kedokteran Jiwa', 'Sp. M': 'Mata',
    'Sp. N': 'Neurologi', 'Sp. OG': 'Obstetri & Ginekologi', 'Sp. OT': 'Orthopedi & Traumatologi',
    'Sp. P': 'Paru', 'Sp. PD': 'Penyakit Dalam', 'Sp. PD.BIOMED': 'Penyakit Dalam (Biomedik)',
    'Sp. PK': 'Patologi Klinik', 'Sp. RAD': 'Radiologi', 'Sp. S': 'Saraf',
    'Sp. THT-BKL': 'THT - Bedah Kepala Leher', 'Umum': 'Dokter Umum',
}

def extract_spec(name):
    n = name.strip()
    m = re.search(r'sp\.?\s*([a-z][a-z\.\-\s/]*)', n, re.IGNORECASE)
    if not m:
        return 'Umum'
    raw = m.group(1).split(',')[0]
    raw = re.sub(r'\s+', ' ', raw).strip(' .')
    raw = raw.upper().replace('K.F.R', 'KFR').replace('K F R', 'KFR')
    return 'Sp. ' + raw if raw else 'Umum'

people = []
for name in DOC.list():
    isd = is_doctor(name)
    spec = extract_spec(name) if isd else None
    people.append({
        'name': name,
        'is_doctor': isd,
        'spec': spec,
        'spec_label': SPEC_FULL.get(spec, spec) if spec else None,
    })

out = {
    'months': [m for m, _ in FILES],
    'people': people,
    'dict': {
        'tindakan': TIND.list(),
        'subklas': SUB.list(),
        'kso': KSO.list(),
        'unit': UNIT.list(),
        'obat': OBAT.list(),
        'date': DATE.list(),
        'dr_anestesi': ANES.list(),
        'rm': RM.list(),
        'pasien': PASIEN.list(),
        'no_penjualan': NOPJ.list(),
    },
    'tRows': t_rows,
    'oRows': o_rows,
    'tDetail': t_detail,
    'oDetail': o_detail,
}

out_path = os.path.join(BASE, 'data_v5.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, separators=(',', ':'))

print("doctors:", len(people))
print("tindakan dict:", len(TIND.list()), "subklas:", len(SUB.list()), "kso:", KSO.list(), "unit:", len(UNIT.list()), "obat:", len(OBAT.list()))
print("dr_anestesi:", ANES.list())
print("dates:", len(DATE.list()), sorted(DATE.list())[:3], '...', sorted(DATE.list())[-3:])
print("t_rows (grouped):", len(t_rows))
print("o_rows (grouped):", len(o_rows))
print("t_detail (rinci):", len(t_detail), "unique RM:", len(RM.list()), "unique Pasien:", len(PASIEN.list()))
print("o_detail (rinci):", len(o_detail), "unique No Penjualan:", len(NOPJ.list()))
print("output size MB:", os.path.getsize(out_path) / 1024 / 1024)
