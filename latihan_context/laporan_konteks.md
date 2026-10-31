# Laporan Eksperimen Context Engineering — Minggu 12

Tanggal: TODO
Model: `qwen2.5:1.5b`
Hardware: Intel Core i7-1195G7, RAM 7,7 GB, NVIDIA MX450 2 GB VRAM
Ollama: TODO (versi)

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
- Setiap posisi dijalankan satu kali.

---

## 3. Hasil

| Posisi | Token dokumen | Jawaban model | Benar? | Latency |
|---|---:|---|---:|---:|
| Awal | TODO | TODO | TODO | TODO |
| Tengah | TODO | TODO | TODO | TODO |
| Akhir | TODO | TODO | TODO | TODO |

---

## 4. Analisis

TODO: jawab pertanyaan berikut.

1. Posisi mana yang paling akurat? Posisi mana yang paling buruk?
2. Apakah hasilnya mendukung fenomena *lost in the middle*? Jelaskan dengan data.
3. Apakah model benar-benar “lupa”, atau hanya gagal mengikuti instruksi
   “balas hanya kodenya”?
4. Faktor apa lagi yang bisa memengaruhi hasil? Sebutkan minimal dua.
5. Mengapa satu kali percobaan belum cukup untuk menyimpulkan kemampuan model?

---

## 5. Implikasi untuk Proyek #4

TODO: hubungkan hasil ini dengan desain summarizer dokumen.

- Di mana informasi penting sebaiknya diletakkan dalam prompt?
- Apa yang harus dilakukan jika dokumen lebih panjang dari context window?
- Bagaimana cara memeriksa bahwa ringkasan tidak kehilangan detail penting?

---

## 6. Refleksi

TODO: tulis 2–3 pelajaran yang kamu dapat, bukan ringkasan ulang hasil.
