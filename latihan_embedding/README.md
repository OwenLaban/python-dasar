# Lab Minggu 13 — Embeddings

Status: 🚧 sedang dikerjakan

Tujuan: memahami bahwa **makna teks bisa direpresentasikan sebagai vektor**,
lalu memakai kedekatan vektor untuk mencari kalimat yang relevan secara
semantik — bukan hanya mencocokkan kata yang sama.

Minggu 12 mengatur konteks yang masuk ke model. Minggu ini kita belajar
representasi makna yang nanti menjadi dasar RAG di Minggu 15–16.

## File

```text
latihan_embedding/
├── README.md                 # instruksi ini
├── materi.md                 # konsep embedding + cosine similarity
├── vektor.py                 # 6 fungsi TODO
├── test_vektor.py            # test tanpa model/jaringan
├── klien_embedding.py        # klien Ollama (sudah jadi)
├── kalimat.py                # 20 kalimat + 4 query
├── eksperimen_embedding.py   # script semantic search
├── laporan_embedding.md      # laporan yang kamu isi
└── hasil_embedding.json      # hasil mentah (dibuat setelah eksperimen)
```

## Model

Lab ini memakai **`nomic-embed-text`** lewat Ollama:

```powershell
ollama pull nomic-embed-text
```

Alasannya:

- hanya sekitar **274 MB**, cocok untuk RAM 7,7 GB dan VRAM 2 GB;
- menghasilkan vektor **768 dimensi**;
- tidak butuh API key dan tidak perlu install PyTorch;
- konsepnya sama dengan model embedding populer lain (OpenAI, Sentence
  Transformers, BGE).

Kalau ingin membandingkan, kamu bisa mencoba model embedding lain lewat
`--model`, misalnya `mxbai-embed-large` atau `bge-m3` (lebih besar).

## Alur

1. Baca `materi.md`.
2. Implementasikan 6 fungsi di `vektor.py` sampai test hijau:

   ```powershell
   .\.venv\Scripts\python.exe -m pytest latihan_embedding -v
   ```

3. Jalankan eksperimen semantic search:

   ```powershell
   .\.venv\Scripts\python.exe -m latihan_embedding.eksperimen_embedding
   ```

4. Isi `laporan_embedding.md` berdasarkan hasil nyata.
5. Commit hasilnya.

## Tugas

| # | Tugas | Bukti |
|---|---|---|
| 1 | Implementasikan `dot_product()` | test lulus |
| 2 | Implementasikan `norm()` | test lulus |
| 3 | Implementasikan `cosine_similarity()` + validasi | test lulus |
| 4 | Implementasikan `normalisasi()` | test lulus |
| 5 | Implementasikan `cari_terdekat()` | test lulus |
| 6 | Implementasikan `precision_at_k()` | test lulus |
| 7 | Jalankan semantic search 20 kalimat | `hasil_embedding.json` |
| 8 | Isi laporan analisis | `laporan_embedding.md` |

## Cara Menilai Hasil

- **precision@3**: berapa dari 3 hasil teratas yang topiknya sesuai.
- **Top-1**: apakah hasil paling atas sudah relevan.
- **Kegagalan menarik**: query yang hasilnya meleset, atau kalimat yang mirip
  kata tetapi berbeda makna.

Jangan hanya melihat skor tinggi. Periksa juga apakah hasilnya benar-benar
relevan bagi manusia.

## Rubrik

| Kriteria | Pertanyaan |
|---|---|
| Fungsional | 6 fungsi lulus test? |
| Pemahaman | Bisa menjelaskan cosine similarity dan normalisasi? |
| Eksperimen | Semantic search dijalankan dan hasilnya dicatat? |
| Analisis | Bisa menjelaskan query yang berhasil dan yang gagal? |
| Kejujuran | Menyebut batasan model dan metrik yang dipakai? |

## Catatan

- Tidak perlu API key; semua berjalan lokal lewat Ollama.
- Embedding bukan database. Di Minggu 14 kita baru menyimpan vektor di vector DB.
- Cosine similarity mengukur kedekatan makna, **bukan kebenaran** fakta.
- Jangan menempelkan API key/secret ke kode, test, atau laporan.
