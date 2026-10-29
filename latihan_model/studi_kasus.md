# Studi Kasus — Pilih Model yang Tepat

Untuk setiap skenario, pilih **2–3 kandidat model**, lalu tentukan satu
rekomendasi. Kamu boleh memakai model yang belum ada di OpenRouter (misalnya
model self-hosted), asalkan alasannya jelas.

---

## Skenario A — Chatbot support Bahasa Indonesia

Sebuah SaaS kecil punya 500 percakapan per hari. Rata-rata satu percakapan
memakai 800 token input dan menghasilkan 300 token output. Chatbot harus:

- menjawab dalam bahasa Indonesia yang natural;
- membalas dalam < 3 detik;
- mengembalikan JSON tiket (`topik`, `sentimen`, `butuh_eskalasi`);
- biaya maksimal **$20/bulan**;
- data pelanggan tidak boleh dipakai untuk training.

**Pertanyaan:** model apa yang kamu pilih? Bandingkan minimal satu model closed
API dan satu model open-weight (lewat API atau self-hosted).

---

## Skenario B — Ringkas kontrak hukum 100k token

Firma hukum memproses 50 kontrak per hari. Satu kontrak panjangnya
80.000–120.000 token. Mereka butuh:

- ringkasan akurat + pasal yang relevan;
- tidak boleh mengarang (halusinasi = risiko hukum);
- context window minimal 128.000 token;
- budget **$200/bulan**;
- dokumen klien **sangat rahasia**.

**Pertanyaan:** apakah kamu memakai API publik, private cloud, atau self-hosted?
Model apa? Jelaskan bagaimana kamu menangani dokumen yang lebih panjang dari
context window.

---

## Skenario C — Asisten catatan medis offline

Klinik di daerah punya satu workstation dengan **RTX 4060 8 GB VRAM**.
Internet tidak stabil, dan data pasien tidak boleh keluar dari klinik. Tugas:

- ringkas catatan dokter;
- ekstrak field JSON (keluhan, diagnosa, tindakan);
- volume 100 catatan/hari;
- latency 10–30 detik masih dapat diterima;
- kualitas harus cukup untuk dibaca manusia, tetapi tetap diperiksa dokter.

**Pertanyaan:** model open-weight apa yang realistis berjalan di 8 GB VRAM?
Apakah kamu memakai model full precision, quantized, atau API lokal? Apa
tradeoff-nya?

---

## Format rekomendasi

Untuk tiap skenario, isi:

1. **Constraint utama** — apa yang tidak boleh dilanggar.
2. **Kandidat** — 2–3 model + jenisnya (closed API / open-weight API /
   self-hosted).
3. **Perbandingan** — harga, context, kualitas perkiraan, privasi, operasional.
4. **Pilihan akhir** — satu model, plus alasan.
5. **Risiko** — apa yang bisa membuat pilihan ini gagal.
