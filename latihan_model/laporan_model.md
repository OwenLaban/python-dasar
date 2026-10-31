# Laporan Pemilihan Model — Minggu 10

Tanggal akses katalog: 29/10/2026
Sumber harga: https://openrouter.ai/models

---

## 1. Ringkasan

Prinsip saya: pilih model berdasarkan **constraint yang paling sulit dipenuhi**,
bukan berdasarkan harga termurah atau context window terbesar. Untuk prototipe,
model gratis bisa dipakai. Untuk data sensitif, privasi dan keandalan
mengalahkan harga. Setiap pilihan tetap harus diuji pada tugas nyata, karena
benchmark publik belum tentu mencerminkan bahasa Indonesia dan format JSON yang
dibutuhkan.

---

## 2. Skenario A — Chatbot support Bahasa Indonesia

### Constraint utama

- Bahasa Indonesia natural.
- Output JSON valid.
- Latency < 3 detik.
- Budget maksimal **$20/bulan**.
- Data pelanggan tidak boleh dipakai untuk training.

### Kandidat

| Model | Jenis | Harga input/M | Harga output/M | Context | Dukung JSON? |
|---|---|---|---:|---:|---|
| `recursive/flint-v1.0:free` | open-weight, API gratis | $0 | $0 | 262k | Ya |
| `google/gemma-4-31b-it:free` | open-weight, API gratis | $0 | $0 | 262k | Ya |
| `openai/gpt-oss-20b` | open-weight, API berbayar | $0.02 | $0.09 | 131k | Ya |

### Pilihan akhir

Untuk **prototipe** saya memilih `recursive/flint-v1.0:free`: gratis, context
262k cukup untuk satu percakapan, dan mendukung `response_format`.

Namun untuk **produksi** saya akan mempertimbangkan `openai/gpt-oss-20b`.
Dengan 500 chat/hari:

```text
Input : 800 token × 500 × 30 = 12 juta token/bulan
Output: 300 token × 500 × 30 = 4,5 juta token/bulan

12 × $0.02  = $0.24
4,5 × $0.09 = $0.405
Total ≈ $0.65/bulan
```

Biaya itu masih jauh di bawah budget $20, tetapi risikonya lebih kecil
daripada model gratis yang bisa kena rate limit.

### Risiko

- Model gratis bisa kena **rate limit**, tidak punya SLA, dan kebijakan data
  tier gratis perlu dicek sebelum dipakai untuk data pelanggan.
- Kualitas bahasa Indonesia dan kepatuhan JSON belum diuji pada 20–50 contoh
  nyata.
- Model gratis bisa deprecated atau berubah tanpa pemberitahuan.
- **Context window bukan kapasitas volume.** 500 chat/hari tetap dibatasi rate
  limit dan throughput; context window hanya menentukan panjang satu request.

---

## 3. Skenario B — Ringkas kontrak hukum 100k token

### Constraint utama

- Satu dokumen 80k–120k token → butuh context ≥128k **atau** strategi chunking.
- Akurasi tinggi + sitasi ke pasal yang relevan.
- Data klien sangat rahasia.
- Budget **$200/bulan**.

### Kandidat

| Model | Jenis | Harga input/M | Harga output/M | Context | Privasi |
|---|---|---|---:|---:|---|
| `z-ai/glm-5.2` | open-weight, bisa private/self-host | $0.01 | $7.00 | 1M | Tergantung provider; jangan pakai endpoint publik tanpa perjanjian |
| `~deepseek/deepseek-flash-latest` | API proprietary | $0.02 | $1.44 | 1M | Data keluar ke provider; cek kebijakan retensi |
| `google/gemma-4-31b-it:free` | open-weight, API gratis | $0 | $0 | 262k | Tier gratis; tidak cocok untuk data klien |

### Pilihan akhir

Saya memilih **GLM-5.2**, tetapi hanya lewat **private cloud/provider dengan
kebijakan zero-retention**, atau self-hosted. GLM-5.2 tersedia sebagai
open-weight, jadi secara teori bisa dijalankan sendiri. Namun untuk context 1M
dibutuhkan hardware besar, sehingga private cloud lebih realistis.

Dengan asumsi output 2.000 token per dokumen:

```text
Input : 50 × 100k × 30 = 150 juta token/bulan
Output: 50 × 2k × 30   = 3 juta token/bulan

Input : 150 × $0.01 = $1.50
Output: 3 × $7.00   = $21.00
Total ≈ $22.50/bulan
```

Masih di bawah $200, tetapi **privasi tetap penentu utama**, bukan harga.

### Strategi dokumen > context window

- Untuk dokumen 80k–120k token, **long-context langsung** masih muat di GLM
  (1M context).
- Untuk sitasi per pasal, potong dokumen berdasarkan pasal/section, simpan
  metadata sumber, lalu gunakan **retrieval (RAG)** untuk mengambil bagian yang
  relevan. Ringkasan akhir menggabungkan hasil per bagian (**map-reduce**) agar
  struktur global tidak hilang.
- Jika dokumen lebih panjang dari context window, gunakan **hierarchical
  summarization**: ringkas per bagian → ringkas ringkasan → sintesis akhir.
  Jangan hanya memotong dokumen di tengah.

### Risiko

- Halusinasi dan sitasi yang salah; ini risiko hukum, bukan sekadar kualitas.
- Kebocoran data jika provider salah dipilih.
- Output $7/M bisa mahal jika ringkasan dibuat panjang.
- Model long-context bisa “lupa” bagian tengah dokumen (*lost in the middle*),
  jadi kualitas di posisi tengah harus diuji.

---

## 4. Skenario C — Asisten catatan medis offline

### Constraint utama

- Data pasien tidak boleh keluar → **offline/self-hosted**.
- Hardware hanya **8 GB VRAM**.
- Harus mengekstrak JSON.
- Hasil tetap diperiksa dokter.
- Latency 10–30 detik masih boleh.

### Kandidat

| Model | Parameter | Quantization | Perkiraan VRAM | Kualitas | Catatan |
|---|---|---:|---|---|---|
| Llama 3.2 3B Instruct | 3B | Q4_K_M | ~2–3 GB | Cukup untuk ringkasan; JSON dasar | Paling aman di 8 GB, cepat |
| Qwen2.5 7B Instruct | 7B | Q4_K_M | ~4–5 GB + KV cache | Lebih baik | Mepet jika context panjang |
| Gemma 2 9B | 9B | Q4_K_M | ~6–7 GB | Baik | Risiko OOM di 8 GB |

### Pilihan akhir

Saya memilih **Llama 3.2 3B Instruct Q4_K_M** karena paling aman di 8 GB VRAM
dan cepat. Kualitasnya lebih rendah daripada 7B, jadi saya akan memakai
constrained decoding (`format=json`), validasi Pydantic, retry, dan review
dokter.

Jika hasil JSON terlalu sering salah, upgrade berikutnya adalah **Qwen2.5 7B
Instruct Q4_K_M** dengan context pendek agar KV cache tidak melebihi VRAM.

### Risiko

- Model kecil lebih **cepat**, tetapi lebih sering salah field atau berhalusinasi.
- Kualitas bahasa Indonesia untuk istilah medis belum tentu cukup.
- KV cache bisa membuat OOM saat context panjang.
- Tidak boleh dipakai sebagai keputusan medis final tanpa review manusia.

---

## 5. Perbandingan lintas skenario

| Kriteria | Paling penting di skenario | Model yang menang |
|---|---|---|
| Biaya | A — volume tinggi | `recursive/flint` (prototipe) atau `gpt-oss-20b` (produksi) |
| Kualitas | B — kontrak hukum | GLM-5.2, dengan syarat privasi |
| Latency | A — chat interaktif | Llama 3B lokal / model kecil |
| Privasi | C — data medis | Llama 3B self-hosted |
| Kemudahan operasional | A — tim kecil | API terkelola, bukan self-hosted |

---

## 6. Refleksi

1. **Kapan self-hosted lebih masuk akal daripada API?**
   Ketika data tidak boleh keluar, volume stabil, dan ada hardware serta tim
   yang bisa merawat server. API lebih masuk akal saat volume fluktuatif dan
   tim ingin fokus ke produk.

2. **Kenapa model termurah belum tentu pilihan terbaik?**
   Karena harga per token bukan satu-satunya biaya. Ada rate limit, kualitas
   yang lebih rendah, biaya retry, risiko privasi, dan hilangnya waktu saat
   model bermasalah.

3. **Kriteria apa yang paling sering saya abaikan, dan apa risikonya?**
   Kebijakan data dan rate limit. Dua hal ini bisa membuat chatbot down atau
   membuat data sensitif keluar tanpa disadari.

4. **Bagaimana cara memilih model untuk proyek berikutnya?**
   Tentukan constraint → shortlist 2–3 model → uji pada 20–50 contoh nyata →
   hitung biaya dan latency → baru pilih. Jangan mulai dari “model terbaik”,
   mulai dari kebutuhan.
