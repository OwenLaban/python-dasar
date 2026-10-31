# Lab Minggu 12 — Context Engineering

Status: 🚧 sedang dikerjakan

Tujuan: memahami bahwa kualitas jawaban LLM tidak hanya ditentukan oleh prompt,
tetapi juga oleh **informasi apa yang dimasukkan ke context window**, berapa
banyak, dan di posisi mana.

Minggu 11 menjalankan model lokal. Minggu ini kita mengatur konteks yang masuk
ke model, lalu memakai konsep itu untuk proyek summarizer dokumen.

## File

```text
latihan_context/
├── README.md              # instruksi ini
├── materi.md              # konsep context engineering + failure modes
├── konteks.py             # 6 fungsi TODO
├── test_konteks.py
├── eksperimen_konteks.py  # eksperimen lost-in-the-middle (sudah jadi)
├── laporan_konteks.md     # laporan yang kamu isi
└── hasil_konteks.json     # hasil mentah (dibuat setelah eksperimen)
```

## Alur

1. Baca `materi.md`.
2. Implementasikan 6 fungsi di `konteks.py` sampai test hijau:

   ```powershell
   .\.venv\Scripts\python.exe -m pytest latihan_context -v
   ```

3. Jalankan eksperimen dengan model lokal:

   ```powershell
   .\.venv\Scripts\python.exe -m latihan_context.eksperimen_konteks
   ```

4. Isi `laporan_konteks.md` berdasarkan hasil nyata.
5. Commit hasilnya.

## Tugas

| # | Tugas | Bukti |
|---|---|---|
| 1 | Implementasikan `hitung_token()` | test lulus |
| 2 | Implementasikan `potong_token()` + validasi | test lulus |
| 3 | Implementasikan `anggaran_input()` | test lulus |
| 4 | Implementasikan `pilih_strategi()` | test lulus |
| 5 | Implementasikan `pangkas_riwayat()` | test lulus |
| 6 | Implementasikan `gabung_ringkasan()` | test lulus |
| 7 | Jalankan eksperimen 3 posisi | `hasil_konteks.json` |
| 8 | Isi laporan analisis | `laporan_konteks.md` |

## Rubrik

| Kriteria | Pertanyaan |
|---|---|
| Fungsional | 6 fungsi lulus test? |
| Pemahaman | Bisa menjelaskan beda context window, prompt, dan memory? |
| Eksperimen | Hasil 3 posisi dijalankan dan dicatat, bukan dikarang? |
| Analisis | Menghubungkan hasil dengan failure mode yang tepat? |
| Kejujuran | Menyebut batasan eksperimen dan hasil yang tidak konsisten? |

## Catatan

- Lab ini memakai model lokal; tidak perlu API key.
- Eksperimen memakai `num_ctx=2048` agar muat di hardware 2 GB VRAM.
- Satu percobaan bukan bukti kuat. Ini latihan mengamati, bukan benchmark resmi.
- Jangan menempelkan API key/secret ke kode, test, atau laporan.
