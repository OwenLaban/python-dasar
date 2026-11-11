# Lab Minggu 14 — Vector Database

Status: 🚧 sedang dikerjakan

Tujuan: memahami **bagaimana vector database menyimpan, mencari, dan menyaring
embedding** — lalu membandingkannya dengan pencarian brute force buatan
sendiri.

Minggu 13 kita bisa mencari kalimat yang mirip. Minggu ini jawabannya harus
bisa disimpan, disaring berdasarkan metadata, diperbarui, dan dicari dalam
waktu yang tetap singkat saat jumlahnya bertambah.

## File

```text
latihan_vectordb/
├── README.md                  # instruksi ini
├── materi.md                  # konsep vector DB, index, metadata filter
├── vektor_db.py               # 6 fungsi TODO (versi mini, pure Python)
├── test_vektor_db.py          # test tanpa DB, model, atau jaringan
├── dokumen.py                 # 100 dokumen Indonesia + 6 query
├── klien_chroma.py            # pembungkus Chroma (sudah jadi)
├── eksperimen_vectordb.py     # indexing + query + filter + CRUD
├── laporan_vectordb.md        # laporan yang kamu isi
├── hasil_vectordb.json        # hasil mentah (dibuat setelah eksperimen)
└── .chroma/                   # folder data Chroma (tidak di-commit)
```

## Instalasi

```powershell
.\.venv\Scripts\python.exe -m pip install chromadb
```

Chroma jalan **embedded** (dalam proses Python), tanpa Docker dan tanpa API
key. Data disimpan di folder `latihan_vectordb/.chroma`.

## Model

Embedding tetap dihitung lokal lewat Ollama:

```powershell
ollama pull bge-m3
```

`bge-m3` dipilih karena **multibahasa** (1024 dimensi). Minggu 13 kita
membuktikan `nomic-embed-text` gagal pada teks Indonesia, dan lab ini memakai
100 dokumen Indonesia — jadi model yang cocok dengan bahasa data itu wajib.

Bisa juga membandingkan:

```powershell
python -m latihan_vectordb.eksperimen_vectordb --model nomic-embed-text
```

## Alur

1. Baca `materi.md`.
2. Implementasikan 6 fungsi di `vektor_db.py` sampai test hijau:

   ```powershell
   .\.venv\Scripts\python.exe -m pytest latihan_vectordb -v
   ```

3. Jalankan eksperimen (butuh Ollama aktif):

   ```powershell
   .\.venv\Scripts\python.exe -m latihan_vectordb.eksperimen_vectordb
   ```

4. Isi `laporan_vectordb.md` berdasarkan hasil nyata.
5. Commit hasilnya.

## Tugas

| # | Tugas | Bukti |
|---|---|---|
| 1 | Implementasikan `id_stabil()` | test lulus |
| 2 | Implementasikan `normalisasi_metadata()` | test lulus |
| 3 | Implementasikan `siapkan_koleksi()` | test lulus |
| 4 | Implementasikan `filter_metadata()` | test lulus |
| 5 | Implementasikan `cari_semantik()` | test lulus |
| 6 | Implementasikan `statistik_koleksi()` | test lulus |
| 7 | Index 100 dokumen ke Chroma, jalankan 6 query | `hasil_vectordb.json` |
| 8 | Coba metadata filter + tambah/perbarui/hapus | `hasil_vectordb.json` |
| 9 | Isi laporan analisis | `laporan_vectordb.md` |

## Cara Menilai Hasil

- **precision@3**: berapa dari 3 hasil teratas yang kategorinya sesuai.
- **Naive vs Chroma**: apakah hasilnya sama? Mana yang lebih cepat?
- **Filter**: apakah benar-benar menyaring sebelum/sesudah pencarian?
- **CRUD**: apakah jumlah dokumen berubah sesuai ekspektasi?

Jangan hanya membandingkan skor. Periksa juga apakah top-3 benar-benar
relevan bagi manusia.

## Rubrik

| Kriteria | Pertanyaan |
|---|---|
| Fungsional | 6 fungsi lulus test? |
| Pemahaman | Bisa menjelaskan index, metadata filter, dan jarak cosine? |
| Eksperimen | 100 dokumen ter-index dan 6 query dievaluasi? |
| Analisis | Bisa menjelaskan ketika index ternyata belum pays off? |
| Kejujuran | Menyebut batasan model, metrik, dan lingkungan yang dipakai? |

## Catatan

- Semua berjalan lokal: tidak ada API key, tidak ada biaya.
- Folder `.chroma/` jangan di-commit (sudah masuk `.gitignore`).
- Vektor dikirim apa adanya ke Chroma, jadi tidak ada model yang diunduh
  diam-diam oleh Chroma.
- Metadata Chroma hanya menerima `str`, `int`, `float`, `bool` — list harus
  diubah jadi string.
- Index HNSW bukan selalu lebih baik. Untuk 100 dokumen, ukur dulu.
