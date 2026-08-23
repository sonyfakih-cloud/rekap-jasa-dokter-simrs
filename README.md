# Rekam Jasa Dokter — Dashboard SIMRS

Dashboard remunerasi jasa dokter RSUD dr. R. Soeprapto Cepu, sumber data 6 sheet
`TABEL IL ITL KRM N OB` + `TABEL KRM OB` bulanan (format `.xlsb`).

## ⚠️ Sebelum push ke GitHub — baca ini dulu

Repo ini direncanakan **PUBLIC** dengan GitHub Pages. Konsekuensinya:

- **`index.html` akan bisa dilihat siapa saja di internet yang tahu URL-nya** (termasuk
  bisa terindeks mesin pencari). File ini berisi seluruh data jasa/pendapatan per
  tindakan per dokter (bukan cuma ringkasan) — ini adalah keputusan yang sudah
  diambil sadar oleh pemilik data.
- **`data_source/` TIDAK BOLEH ikut ter-commit dalam kondisi apa pun.** Folder ini
  berisi file mentah `.xlsb`, `data_v5.json`, dan 2 file Excel rinci
  (`Tindakan_Rinci_SemuaDokter.xlsx`, `Obat_Rinci_SemuaDokter.xlsx`) yang memuat
  **No RM dan Nama Pasien** — data pasien sungguhan. Ini beda kategori dari data
  pendapatan dokter: kebocoran data pasien berpotensi melanggar kerahasiaan medis.
  `.gitignore` di repo ini sudah mengecualikan folder tsb — jangan dihapus/di-override.

Kalau ternyata butuh akses terbatas (bukan publik penuh), opsinya: jadikan repo
private (perlu GitHub Pro/Team/Enterprise agar GitHub Pages private-nya jalan), atau
tetap gunakan Artifact link yang sudah ada (privat secara default, tidak terindeks).

## Struktur repo

```
index.html              <- dashboard jadi (satu file, self-contained). Inilah yang
                            dilayani GitHub Pages. Di-generate oleh scripts/build.py.
scripts/
  extract_all.py         <- baca 6 file .xlsb -> data_source/data_v5.json
  build.py                <- data_source/data_v5.json -> index.html (ringan, tanpa
                              data pasien, ~8-9MB)
  export_detail_excel.py  <- data_source/data_v5.json -> 2 file .xlsx rinci per-kunjungan
                              (utk didistribusikan manual via chat/Drive, BUKAN ke git)
  requirements.txt
data_source/             <- (di-gitignore) taruh file .xlsb bulanan + hasil olahan di sini
```

## Setup awal

```bash
python3 -m pip install -r scripts/requirements.txt
mkdir -p data_source
```

Salin 6 file `.xlsb` dari Google Drive folder **"TENAGA MEDIS SIMRS POIN"**
(`drive.google.com/drive/folders/1409SWJJBO0aVQaG7Ua6XQfyu72sWRBTn`) ke folder
`data_source/`, dengan nama file persis sama seperti terdaftar di
`scripts/extract_all.py` (`FILES = [...]`).

## Generate / update dashboard

```bash
python3 scripts/extract_all.py          # data_source/*.xlsb -> data_source/data_v5.json
python3 scripts/build.py                # data_source/data_v5.json -> index.html
python3 scripts/export_detail_excel.py  # (opsional) -> 2 file .xlsx rinci di data_source/
```

Lalu commit & push **hanya** `index.html` (dan perubahan di `scripts/` kalau ada):

```bash
git add index.html scripts/
git commit -m "Update dashboard: data s.d. <bulan>"
git push
```

## Update bulanan (data baru masuk)

1. Download file `.xlsb` bulan baru dari Google Drive folder di atas ke `data_source/`.
2. Tambahkan satu baris baru ke daftar `FILES` di `scripts/extract_all.py`, misalnya:
   ```python
   ('2026-07', 'TEMPLATE KSI JULI 2026 BASIS TARIF MURNI BARU.xlsb'),
   ```
3. Jalankan ulang 2 perintah di atas (`extract_all.py` lalu `build.py`).
4. Commit & push `index.html` (+ perubahan `scripts/extract_all.py`).

## Mengaktifkan GitHub Pages

Repo → **Settings → Pages** → Source: `Deploy from a branch` → Branch: `main` /
folder `/ (root)` → Save. URL situs akan muncul di halaman yang sama
(`https://<username>.github.io/<nama-repo>/`), aktif dalam 1-2 menit setelah push.

## Catatan fitur dashboard

- Tab **Data Dokter**: KPI, rincian jasa per komponen, tren biaya tindakan per bulan,
  tabel Tindakan Dilaksanakan (Unik) & Obat, deteksi "Dokter Anestesi" (kolom BB,
  khusus subklasifikasi Tindakan Medis Operatif). Filter Unit & Tindakan (grafik
  tren) di-scope otomatis ke baris yang japel>0 atau operator>0.
- Tab **Perbandingan Spesialisasi**: membandingkan semua dokter dalam satu
  spesialisasi, dengan filter KSO/Unit/rentang tanggal/tindakan unik, plus rincian
  Tindakan & Obat per dokter (struktur sama dgn tab Data Dokter).
- Data rinci per-kunjungan/per-transaksi (No RM, Nama Pasien) **sengaja tidak**
  disematkan di `index.html` — tersedia sbg 2 file Excel terpisah (lihat
  `export_detail_excel.py`), didistribusikan manual, bukan lewat repo publik ini.
