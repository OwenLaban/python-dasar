# Lab Minggu 11 — Hugging Face + Model Lokal

Tujuan: memahami **di mana model berasal** (Hugging Face Hub) dan **bagaimana
menjalankannya sendiri** (Ollama), lalu membandingkan 3 model pada tugas yang
sama.

Minggu 10 memilih model dari katalog API. Minggu ini kamu melihat metadata model
di Hugging Face dan menjalankan model open-weight di laptop sendiri.

## File

```text
latihan_lokal/
├── README.md              # instruksi ini
├── tugas.md               # tugas ekstraksi tiket + rubrik
├── hf_explorer.py         # 5 fungsi TODO
├── test_hf_explorer.py
├── benchmark_ollama.py    # script benchmark (sudah jadi)
├── test_benchmark_ollama.py
└── laporan_benchmark.md   # laporan yang kamu isi
```

## Prasyarat

- Ollama terpasang.
- Model sudah di-pull:

  ```powershell
  ollama pull llama3.2:1b
  ollama pull qwen2.5:1.5b
  ollama pull gemma2:2b
  ```

Hardware laptop ini: **2 GB VRAM + 7,7 GB RAM**. Model 1B–2B quantized masih
realistis; 7B akan sangat lambat atau kehabisan memori.

## Alur

1. Baca `tugas.md`.
2. Implementasikan 5 fungsi di `hf_explorer.py`.
3. Jalankan test sampai hijau:

   ```powershell
   .\.venv\Scripts\python.exe -m pytest latihan_lokal -v
   ```

4. Jelajahi Hugging Face Hub:

   ```powershell
   .\.venv\Scripts\python.exe -m latihan_lokal.hf_explorer
   ```

5. Jalankan benchmark 3 model:

   ```powershell
   .\.venv\Scripts\python.exe -m latihan_lokal.benchmark_ollama
   ```

6. Isi `laporan_benchmark.md`.
7. Commit hasilnya.

## Yang dilatih

- Membaca metadata Hugging Face: task, library, license, gated, parameter count.
- Membedakan **model card** (dokumentasi) dari **bobot model** (file).
- Menjalankan model lokal lewat HTTP API Ollama.
- Mengukur latency, validitas JSON, dan kualitas output pada tugas nyata.
- Menghubungkan ukuran model dengan batas VRAM/RAM.

## Rubrik penilaian

| Kriteria | Pertanyaan |
|---|---|
| Fungsional | 5 fungsi HF lulus test? |
| Benchmark | 3 model dijalankan pada prompt yang sama? |
| Akurasi | JSON valid dan field lengkap? |
| Analisis | Perbandingan latency, kualitas, dan ukuran model masuk akal? |
| Kejujuran | Keterbatasan dan kegagalan model disebut? |

## Catatan

- Metadata Hugging Face publik tidak butuh token.
- Jangan menempelkan token/API key ke kode, test, atau laporan.
- Endpoint list HF **tidak selalu** menyertakan jumlah parameter. Detail model
  (`/api/models/{id}`) yang menyertakannya — ini salah satu pelajaran lab.
