# Laporan Eksperimen Context Engineering — Minggu 12

Tanggal: 31/10/2026
Model: `qwen2.5:1.5b`
Hardware: Intel Core i7-1195G7, RAM 7,7 GB, NVIDIA MX450 2 GB VRAM
Ollama: 0.40.13

---

## 1. Pertanyaan

Apakah posisi sebuah informasi di dalam dokumen memengaruhi kemampuan model
untuk menemukannya?

Eksperimen ini menaruh kode rahasia `BIRU-4721` di **awal**, **tengah**, dan
**akhir** dokumen. Model diminta membalas hanya kode tersebut.

---

## 2. Metode

- Dokumen berisi 60 baris catatan operasional yang tidak relevan.
- Satu baris berisi kode rahasia.
- Prompt, model, temperature, dan `num_ctx` sama untuk ketiga posisi.
- Total prompt sekitar 1.627 token, sedangkan `num_ctx` 2.048 token.
- Temperature 0 dan `num_predict` 20.
- Setiap posisi dijalankan satu kali, berurutan: awal → tengah → akhir.
- Keterbatasan: satu model, satu dokumen sintetis, dan satu run per posisi.

---

## 3. Hasil

| Posisi | Token prompt | Jawaban model | Benar? | Latency |
|---|---:|---|---:|---:|
| Awal | 1627 | `32` | Tidak | 22,28 s |
| Tengah | 1627 | `32` | Tidak | 2,29 s |
| Akhir | 1627 | `BIRU-4721` | Ya | 5,78 s |

Catatan: latency posisi awal tidak sebanding dengan posisi lain karena run
pertama masih mencakup **cold start**, yaitu waktu memuat model ke memori.
Latency tidak dipakai untuk menilai akurasi.

---

## 4. Analisis

1. **Posisi mana yang paling akurat?**
   Hanya posisi akhir yang benar. Posisi awal dan tengah sama-sama menghasilkan
   `32`, bukan kode rahasia.

2. **Apakah hasilnya mendukung fenomena *lost in the middle*?**
   Tidak secara bersih. *Lost in the middle* biasanya terlihat saat informasi
   di awal dan akhir berhasil ditemukan, sedangkan informasi di tengah gagal.
   Di sini posisi awal juga gagal, sehingga hasil belum bisa menjelaskan
   pengaruh posisi secara terpisah. Hasil ini lebih aman disebut sebagai
   **kegagalan retrieval pada dua posisi pertama**, yang bisa dipengaruhi
   urutan prompt, filler, dan keterbatasan model.

3. **Apakah model benar-benar “lupa” atau gagal mengikuti instruksi?**
   Model mengalami dua kegagalan sekaligus:
   - gagal mengambil kode rahasia yang benar;
   - gagal mengikuti format `KATA-ANGKA`.

   Jawaban `32` kemungkinan besar terambil dari filler
   “Catatan operasional nomor 32”. Jadi ini bukan bukti sederhana bahwa model
   “lupa”, melainkan **distraction** dari pola angka yang berulang sekaligus
   kegagalan mengikuti instruksi.

4. **Faktor lain yang bisa memengaruhi hasil:**
   - filler repetitif dan bernomor, sehingga model mudah terpancing pola angka;
   - kapasitas model 1,5B yang terbatas untuk retrieval di konteks panjang;
   - hanya satu run per posisi;
   - pertanyaan diletakkan setelah dokumen, sehingga posisi instruksi juga
     memengaruhi perhatian model;
   - total prompt 1.627 token masih muat dalam `num_ctx` 2.048, jadi hasil ini
     **bukan** disebabkan overflow;
   - cold start memengaruhi latency, tetapi tidak menjelaskan perbedaan isi
     jawaban.

5. **Mengapa satu kali percobaan belum cukup?**
   Output LLM dapat berubah karena sampling, kondisi mesin, thermal throttling,
   dan sensitivitas terhadap prompt. Satu run tidak cukup untuk memisahkan
   pengaruh posisi dari faktor-faktor tersebut. Diperlukan beberapa run,
   variasi filler, dan model pembanding.

---

## 5. Implikasi untuk Proyek #4

- **Penempatan informasi penting:** letakkan instruksi dan pertanyaan di akhir
  prompt, lalu ulangi fakta kunci di awal dan akhir. Jangan mengandalkan satu
  posisi saja; hasil eksperimen ini belum cukup untuk menggeneralisasi.
- **Dokumen lebih panjang dari context window:** potong dengan overlap, lalu
  gunakan **map-reduce** (ringkas tiap potongan, gabungkan) atau **refine**
  (perbarui ringkasan bertahap). Jangan hanya memotong dokumen dan berharap
  detail penting tetap ada.
- **Memeriksa detail yang hilang:** gunakan daftar fakta kunci atau ground
  truth, bandingkan hasil ringkasan dengan sumber, dan lakukan pemeriksaan
  manual. Temperature 0 hanya mengurangi variasi; ia tidak menjamin
  kelengkapan atau kebenaran isi.

---

## 6. Refleksi

Posisi informasi memang bisa memengaruhi jawaban, tetapi hasil satu run tidak
cukup untuk menyimpulkan sebabnya. Model kecil juga mudah terpancing pola
dalam konteks, bukan hanya “lupa” pada informasi yang benar.

Pelajaran utamanya: context engineering harus disertai evaluasi. Kita perlu
menguji beberapa run, menyiapkan pembanding, dan memeriksa isi jawaban — bukan
hanya memastikan prompt muat di context window. Pengukuran latency juga harus
memisahkan cold start dari performa steady-state.
