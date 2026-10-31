# Laporan Benchmark Model Lokal — Minggu 11

Tanggal: 31/10/2026
Hardware: Intel Core i7-1195G7 (4 core / 8 thread), RAM 7,7 GB, NVIDIA MX450 2 GB VRAM
Ollama: 0.40.13

---

## 1. Tugas

Ekstraksi tiket dari email pelanggan menjadi JSON dengan 5 field:
`nama`, `email`, `topik`, `sentimen`, `butuh_eskalasi`.

Prompt dan email lengkap ada di [`tugas.md`](tugas.md).

---

## 2. Model yang Dibandingkan

| Model | Parameter | Ukuran unduhan | Context | Quantization |
|---|---:|---:|---:|---|
| `llama3.2:1b` | 1,2B | 1,3 GB | 128k | Q8_0 |
| `qwen2.5:1.5b` | 1,5B | 986 MB | 32k | Q4_K_M |
| `gemma2:2b` | 2,6B | 1,6 GB | 8k | Q4_0 |

Quantization di atas adalah default paket Ollama, bukan pilihan yang disamakan.
Ini penting: `llama3.2:1b` memakai Q8_0 (lebih presisi dan lebih besar per
parameter), sedangkan dua model lain memakai quantized 4-bit.

---

## 3. Hasil

| Model | Latency (s) | Token/detik | JSON valid? | Field lengkap? | Nilai kualitas (1–5) |
|---|---:|---:|---|---|---:|
| `llama3.2:1b` | 19,64 | 17,44 | Ya | Ya | 3 |
| `qwen2.5:1.5b` | 10,79 | 25,68 | Ya | Ya | 5 |
| `gemma2:2b` | 16,64 | 10,87 | Ya | Ya | 5 |

Catatan: latency diukur pada run kedua (setelah model dimuat ke memori).
Run pertama dipakai sebagai warm-up agar perbandingan antar model lebih adil.
Nilai kualitas menimbang kebenaran isi, bukan hanya format JSON.

Sebagai pembanding, run pemanasan menghasilkan: `llama3.2:1b` 16,34 s /
17,26 token/detik, `qwen2.5:1.5b` 11,33 s / 26,50 token/detik, dan
`gemma2:2b` 22,94 s / 10,77 token/detik. Selisih ini menunjukkan bahwa satu
kali pengukuran belum cukup untuk menyimpulkan performa secara umum.

---

## 4. Contoh Output

### llama3.2:1b

```json
{
  "nama": "Rina",
  "email": "rina@sinarjaya.co.id",
  "topik": "Pesanan #4821 belum sampai",
  "sentimen": "negatif",
  "butuh_eskalasi": false
}
```

Catatan: format benar, tetapi `butuh_eskalasi` salah. Pelanggan menyebut
pesanan terlambat untuk acara Jumat dan chat tidak dibalas, jadi nilainya
seharusnya `true`.

### qwen2.5:1.5b

```json
{
  "nama": "Rina",
  "email": "rina@sinarjaya.co.id",
  "topik": "Pesanan tidak sampai",
  "sentimen": "negatif",
  "butuh_eskalasi": true
}
```

Catatan: seluruh field sesuai dengan isi email.

### gemma2:2b

```json
{
  "nama": "Rina",
  "email": "rina@sinarjaya.co.id",
  "topik": "Pesanan belum sampai",
  "sentimen": "negatif",
  "butuh_eskalasi": true
}
```

Catatan: seluruh field sesuai; pilihan kata `topik` sedikit berbeda tetapi
maknanya tetap tepat.

---

## 5. Analisis

`qwen2.5:1.5b` paling seimbang untuk tugas ini. Ia mencatat latency terendah
(10,79 s) dan throughput tertinggi (25,68 token/detik), meskipun parameternya
lebih besar daripada `llama3.2:1b`. Sebagian selisih ini dijelaskan oleh
quantization: llama memakai Q8_0, sedangkan qwen memakai Q4_K_M yang jauh lebih
ringan. Jadi hasil ini bukan perbandingan murni antararsitektur. Faktor lain
tetap berpengaruh: tokenizer, jumlah token yang dihasilkan, dukungan runtime,
dan pembagian kerja CPU/GPU.

Ketiga model menghasilkan JSON valid dan lima field lengkap. Perbedaannya ada
pada kebenaran isi. `llama3.2:1b` memberi topik yang lebih spesifik karena
menyertakan nomor pesanan, tetapi salah menilai kebutuhan eskalasi.

1. **Apakah model terkecil selalu paling cepat?** Tidak. `llama3.2:1b` justru
   lebih lambat (19,64 s; 17,44 token/detik) daripada `qwen2.5:1.5b` (10,79 s;
   25,68 token/detik). Ukuran parameter hanya salah satu faktor; perbedaan
   quantization (Q8_0 vs Q4_K_M), efisiensi arsitektur dan tokenizer, panjang
   output, serta penempatan di CPU/GPU ikut menentukan. Variasi antar-run juga
   terlihat pada llama (16,34 s menjadi 19,64 s), kemungkinan karena kondisi
   mesin saat pengukuran.
2. **Apakah JSON valid otomatis berarti isinya benar?** Tidak. Output llama
   valid secara sintaks dan lengkap, tetapi `butuh_eskalasi` bernilai `false`.
   Validasi schema hanya memeriksa bentuk, bukan kebenaran semantik.
3. **Field apa yang paling sering salah atau kosong?** Tidak ada field kosong.
   Kesalahan yang muncul adalah `butuh_eskalasi` pada llama (1 dari 3 model).
   Nama, email, dan sentimen benar di semua model; `topik` berbeda kata tetapi
   tetap relevan.
4. **Apakah `gemma2:2b` muat di 2 GB VRAM?** Tidak sepenuhnya. Saat model aktif,
   `ollama ps` menunjukkan ukuran 1,9 GB dengan pembagian **94% CPU / 6% GPU**.
   Bobot 1,6 GB menyisakan sekitar 0,4 GB VRAM, tidak cukup untuk KV cache dan
   overhead runtime, sehingga sebagian besar inferensi berjalan di CPU. Ini
   konsisten dengan throughput rendah (10,87 token/detik).

Perlu dicatat bahwa latency dan throughput mengukur hal berbeda: latency
mencakup pemrosesan prompt sampai respons selesai, sedangkan token/detik hanya
mengukur kecepatan generasi. Karena itu `gemma2:2b` bisa punya latency lebih
rendah daripada llama pada run ini meskipun throughput-nya jauh lebih kecil.

---

## 6. Rekomendasi

Pilih **`qwen2.5:1.5b`** untuk tugas ekstraksi tiket ini. Berdasarkan data, ia
paling cepat (10,79 s), punya throughput tertinggi (25,68 token/detik), ukuran
unduhannya paling kecil (986 MB), dan seluruh field benar. `gemma2:2b` juga
akurat, tetapi lebih lambat dan sebagian besar berjalan di CPU; `llama3.2:1b`
salah pada field eskalasi.

Risiko yang perlu disebut:

- Perbandingan memakai quantization default yang berbeda (Q8_0, Q4_K_M, Q4_0),
  jadi kecepatan tidak boleh diatribusikan hanya kepada jumlah parameter.
- Benchmark hanya memakai **satu email dan satu run** untuk data laporan, jadi
  belum cukup untuk menggeneralisasi ke semua tiket.
- Kualitas dinilai manual dan belum memakai dataset uji dengan ground truth.
- Model kecil bisa gagal pada email panjang, bahasa campuran, atau permintaan
  yang ambigu; validasi schema dan aturan eskalasi tetap diperlukan.
- Laptop dengan 2 GB VRAM akan sering jatuh ke CPU, sehingga latency bisa
  berubah karena thermal throttling atau aplikasi lain yang berjalan.
- Untuk produksi, tambahkan validasi field, fallback ke model API jika output
  tidak valid, dan uji regresi dengan lebih banyak contoh.

---

## 7. Refleksi

1. **Apa perbedaan Hugging Face Hub dan Ollama?**
   Hugging Face Hub adalah katalog/repositori tempat model, dataset, dan model
   card dipublikasikan. Ollama adalah runtime lokal yang mengunduh model
   terkuantisasi (umumnya GGUF), memuatnya ke memori, dan menyediakan HTTP API
   untuk inferensi. Hugging Face adalah “gudang sumber model”; Ollama adalah
   “mesin yang menjalankannya” di laptop.
2. **Kapan model lokal lebih masuk akal daripada API?**
   Saat data sensitif tidak boleh keluar perangkat, saat butuh bekerja offline,
   saat volume rendah sehingga biaya per token API tidak sepadan, atau saat
   ingin bereksperimen tanpa bergantung pada kuota dan jaringan. Untuk kualitas
   maksimal, skala besar, atau context sangat panjang, API biasanya lebih
   praktis.
3. **Apa yang akan kamu lakukan berbeda jika hardware-nya 8 GB VRAM?**
   Saya akan menjalankan model 7B–8B quantized (misalnya Qwen2.5 7B atau
   Llama 3.1 8B) sepenuhnya di GPU, membandingkannya dengan model 1–2B, dan
   menguji context yang lebih panjang. Dengan VRAM lebih besar, throughput dan
   kualitas isi bisa meningkat, tetapi validasi output dan evaluasi pada dataset
   kecil tetap harus dilakukan.
