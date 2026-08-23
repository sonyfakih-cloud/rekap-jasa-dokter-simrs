"""
Ekspor data rinci per-kunjungan/per-transaksi (No RM, Nama Pasien, dst) dari
data_source/data_v5.json -> 2 file Excel di data_source/ (TIDAK di-commit ke git --
berisi data pasien, lihat .gitignore).

Jalankan setelah scripts/extract_all.py:  python3 scripts/export_detail_excel.py
"""
import json, time, os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data_source')
DATA_PATH = os.path.join(DATA_DIR, 'data_v5.json')

t0 = time.time()
print("loading data_v5.json ...", flush=True)
data = json.load(open(DATA_PATH, encoding='utf-8'))
d = data['dict']
people = [p['name'] for p in data['people']]
print(f"loaded in {time.time()-t0:.1f}s", flush=True)

# ---------- Tindakan Unik - Rinci per Kunjungan ----------
t1 = time.time()
cols_t = ['Tanggal', 'No RM', 'Nama Pasien', 'Nama KSO', 'Unit', 'Pelaksana', 'Tindakan',
          'Subklasifikasi', 'Qty', 'Japel', 'Jasa Sarana', 'Operator', 'Anestesi', 'Team', 'Poin']
rows_t = []
for r in data['tDetail']:
    dtIdx, rmIdx, pasienIdx, kIdx, uIdx, docIdx, tIdx, sIdx, qty, japel, jsarrs, operator, anestesi, team, biaya = r
    rows_t.append((
        d['date'][dtIdx], d['rm'][rmIdx], d['pasien'][pasienIdx], d['kso'][kIdx], d['unit'][uIdx],
        people[docIdx], d['tindakan'][tIdx], d['subklas'][sIdx], qty, japel, jsarrs, operator, anestesi, team,
        round((japel + operator) / 1000),
    ))
df_t = pd.DataFrame(rows_t, columns=cols_t)
print(f"built tindakan dataframe ({len(df_t)} rows) in {time.time()-t1:.1f}s", flush=True)

t2 = time.time()
out_t = os.path.join(DATA_DIR, 'Tindakan_Rinci_SemuaDokter.xlsx')
with pd.ExcelWriter(out_t, engine='xlsxwriter') as writer:
    df_t.to_excel(writer, index=False, sheet_name='Tindakan Rinci')
print(f"wrote {out_t} in {time.time()-t2:.1f}s", flush=True)

# ---------- Obat - Rinci per Transaksi ----------
t3 = time.time()
cols_o = ['Tanggal', 'No Penjualan', 'Nomor RM', 'Nama Pasien', 'KSO', 'Nama Obat', 'Qty',
          'Harga Total', 'Ruangan', 'Dokter']
rows_o = []
for r in data['oDetail']:
    dtIdx, nopjIdx, rmIdx, pasienIdx, kIdx, obatIdx, qty, hargaTotal, uIdx, docIdx = r
    rows_o.append((
        d['date'][dtIdx], d['no_penjualan'][nopjIdx], d['rm'][rmIdx], d['pasien'][pasienIdx], d['kso'][kIdx],
        d['obat'][obatIdx], qty, hargaTotal, d['unit'][uIdx], people[docIdx],
    ))
df_o = pd.DataFrame(rows_o, columns=cols_o)
print(f"built obat dataframe ({len(df_o)} rows) in {time.time()-t3:.1f}s", flush=True)

t4 = time.time()
out_o = os.path.join(DATA_DIR, 'Obat_Rinci_SemuaDokter.xlsx')
with pd.ExcelWriter(out_o, engine='xlsxwriter') as writer:
    df_o.to_excel(writer, index=False, sheet_name='Obat Rinci')
print(f"wrote {out_o} in {time.time()-t4:.1f}s", flush=True)

print("=== RESULT ===")
print(out_t, round(os.path.getsize(out_t)/1024/1024, 2), "MB")
print(out_o, round(os.path.getsize(out_o)/1024/1024, 2), "MB")
print(f"total time {time.time()-t0:.1f}s")
