# Latihan 15 — Prompt Engineering

Tujuan: membandingkan **5 variasi prompt** untuk satu tugas yang sama, lalu menilai
mana yang paling akurat, konsisten, dan aman.

## Tugas

Ubah email pelanggan menjadi **JSON tiket dukungan** dengan field:

```json
{
  "nama": "string",
  "produk": "string | null",
  "masalah": "string",
  "urgent": true,
  "prioritas": "rendah | sedang | tinggi",
  "ringkasan": "string"
}
```

Aturan output:

- Hanya JSON valid, tanpa markdown fence dan tanpa teks tambahan.
- Jangan mengarang data yang tidak ada; gunakan `null` jika tidak diketahui.
- `urgent` hanya `true` jika ada indikasi mendesak.
- `prioritas` mengikuti aturan di `data_email.md`.

## Alat

Gunakan chatbot gratis lewat web, misalnya ChatGPT, Gemini, atau Claude.

- Tidak perlu API key.
- **Jangan pernah menempelkan API key/secret ke prompt.**
- Pakai **model yang sama** untuk semua variasi agar perbandingannya adil.
- Jangan ubah email input antar-variasi.

## File

```text
latihan_prompt/
├── README.md       # instruksi ini
├── data_email.md   # email uji + kunci evaluasi
└── prompt_lab.md   # tempat menulis 5 prompt dan hasil evaluasi
```

## Alur

1. Baca `data_email.md`.
2. Tulis 5 variasi prompt di `prompt_lab.md`.
3. Jalankan setiap prompt di chatbot dengan **Email 1**.
4. Catat hasilnya di tabel evaluasi.
5. Uji prompt terbaik dengan **Email 2** (edge case).
6. Isi refleksi.
7. Commit hasilnya.

## Rubrik evaluasi

| Kriteria | Pertanyaan |
|---|---|
| JSON valid | Apakah output bisa di-parse sebagai JSON? |
| Format | Apakah hanya JSON, tanpa teks/fence tambahan? |
| Kelengkapan | Apakah semua field ada? |
| Akurasi | Apakah isi field sesuai email? |
| Halusinasi | Apakah model menambah fakta yang tidak ada? |
| Robustness | Apakah tetap benar saat informasi ambigu/kurang? |

## Setelah selesai

Bilang **“cek”**. Kita akan review prompt mana yang paling kuat, lalu jadikan
baseline untuk proyek chatbot di Minggu 9.
