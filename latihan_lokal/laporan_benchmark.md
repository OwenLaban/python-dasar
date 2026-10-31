# Laporan Benchmark Model Lokal — Minggu 11

Tanggal: TODO
Hardware: TODO (CPU, RAM, GPU/VRAM)
Ollama: TODO (versi)

---

## 1. Tugas

Ekstraksi tiket dari email pelanggan menjadi JSON dengan 5 field:
`nama`, `email`, `topik`, `sentimen`, `butuh_eskalasi`.

Prompt dan email lengkap ada di [`tugas.md`](tugas.md).

---

## 2. Model yang Dibandingkan

| Model | Parameter | Ukuran unduhan | Context | Quantization |
|---|---:|---:|---:|---|
| `llama3.2:1b` | TODO | TODO | TODO | TODO |
| `qwen2.5:1.5b` | TODO | TODO | TODO | TODO |
| `gemma2:2b` | TODO | TODO | TODO | TODO |

---

## 3. Hasil

| Model | Latency (s) | Token/detik | JSON valid? | Field lengkap? | Nilai kualitas (1–5) |
|---|---:|---:|---|---|---:|
| `llama3.2:1b` | TODO | TODO | TODO | TODO | TODO |
| `qwen2.5:1.5b` | TODO | TODO | TODO | TODO | TODO |
| `gemma2:2b` | TODO | TODO | TODO | TODO | TODO |

Catatan: latency diukur dari request sampai response selesai, termasuk waktu
memuat model ke memori pada request pertama.

---

## 4. Contoh Output

### llama3.2:1b

```json
TODO
```

### qwen2.5:1.5b

```json
TODO
```

### gemma2:2b

```json
TODO
```

---

## 5. Analisis

TODO: bandingkan latency, validitas JSON, kelengkapan field, dan kualitas isi.
Sebutkan model mana yang paling seimbang untuk tugas ini.

Pertanyaan yang harus dijawab:

1. Apakah model terkecil selalu paling cepat? Mengapa?
2. Apakah JSON valid otomatis berarti isinya benar?
3. Field apa yang paling sering salah atau kosong?
4. Apakah `gemma2:2b` muat di 2 GB VRAM, atau sebagian berjalan di CPU?

---

## 6. Rekomendasi

TODO: pilih satu model untuk tugas ini, lalu jelaskan alasannya berdasarkan
data di atas — bukan berdasarkan kesan umum.

Risiko yang perlu disebut:

- TODO
- TODO

---

## 7. Refleksi

1. Apa perbedaan **Hugging Face Hub** dan **Ollama**?
   TODO
2. Kapan model lokal lebih masuk akal daripada API?
   TODO
3. Apa yang akan kamu lakukan berbeda jika hardware-nya 8 GB VRAM?
   TODO
