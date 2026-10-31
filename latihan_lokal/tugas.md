# Tugas Minggu 11 — Ekstraksi Tiket dari Email

Satu tugas, tiga model. Tujuannya bukan mencari model “terbaik di dunia”, tapi
melihat **tradeoff nyata** di hardware terbatas.

## Tugas

Ekstrak informasi dari email pelanggan berikut menjadi JSON:

```text
Halo tim support,

Saya Rina dari PT Sinar Jaya. Pesanan #4821 yang saya bayar minggu lalu
belum sampai, padahal kurir bilang paket sudah dikirim. Saya sudah coba
chat tapi tidak ada balasan. Tolong dicek ya, ini sudah terlambat untuk
acara kami hari Jumat.

Email: rina@sinarjaya.co.id
```

## Schema output

```json
{
  "nama": "Rina",
  "email": "rina@sinarjaya.co.id",
  "topik": "pesanan belum sampai",
  "sentimen": "negatif",
  "butuh_eskalasi": true
}
```

Aturan:

- `nama`: string atau `null`.
- `email`: string atau `null`.
- `topik`: ringkasan singkat, bukan kalimat panjang.
- `sentimen`: salah satu dari `positif`, `netral`, `negatif`.
- `butuh_eskalasi`: boolean.

## Model yang dibandingkan

| Model | Ukuran | Context | Catatan |
|---|---:|---:|---|
| `llama3.2:1b` | 1,3 GB | 128k | paling kecil |
| `qwen2.5:1.5b` | 986 MB | 32k | multilingual, termasuk Indonesia |
| `gemma2:2b` | 1,6 GB | 8k | paling besar di kelompok ini |

Ketiganya memakai quantization default Ollama, tetapi tidak sama:
`llama3.2:1b` Q8_0, `qwen2.5:1.5b` Q4_K_M, dan `gemma2:2b` Q4_0. Di laptop
dengan 2 GB VRAM, `gemma2:2b` sebagian besar berjalan di CPU.

## Yang dinilai

| Aspek | Cara menilai |
|---|---|
| JSON valid | `json.loads` berhasil |
| Field lengkap | 5 field wajib ada |
| Akurasi isi | Bandingkan dengan email |
| Latency | Dicatat otomatis oleh script |
| Kualitas bahasa | Nilai 1–5 secara manual |
| Catatan | Halusinasi, field salah, output terpotong |

## Laporan

Isi `laporan_benchmark.md`:

1. Spesifikasi laptop.
2. Tabel hasil (latency, JSON valid, field lengkap, nilai kualitas).
3. Contoh output tiap model.
4. Analisis: model mana yang paling seimbang?
5. Rekomendasi untuk tugas ini dan alasannya.
