# Laporan Eksperimen Embedding — Minggu 13

Tanggal: TODO
Model: `nomic-embed-text`
Dimensi: TODO
Hardware: Intel Core i7-1195G7, RAM 7,7 GB, NVIDIA MX450 2 GB VRAM
Ollama: TODO (versi)

---

## 1. Pertanyaan

Apakah embedding bisa menemukan kalimat yang **maknanya relevan** meskipun
kata-katanya tidak sama persis dengan query?

---

## 2. Metode

- 20 kalimat dari 4 topik: teknologi, kuliner, olahraga, keuangan.
- 4 query, masing-masing punya topik target.
- Setiap teks diubah menjadi vektor 768 dimensi dengan `nomic-embed-text`.
- Vektor dinormalisasi, lalu diurutkan dengan cosine similarity.
- Metrik: top-1 relevan dan **precision@3**.

---

## 3. Hasil

| Query | Top-1 | Relevan? | Precision@3 |
|---|---|---|---|
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |

Ringkasan skor:

```text
TODO: tempel output eksperimen di sini
```

---

## 4. Analisis

TODO: jawab pertanyaan berikut.

1. Query mana yang paling berhasil? Mengapa?
2. Query mana yang hasilnya mengejutkan atau meleset?
3. Apakah ada kalimat yang mirip secara kata tetapi berbeda makna?
4. Apakah cosine similarity cukup untuk menilai relevansi? Apa yang hilang?
5. Bandingkan dengan pencarian kata kunci biasa: apa kelebihan dan kekurangan
   embedding?

---

## 5. Use Case

TODO: jelaskan 4 use case embedding dan contoh konkretnya.

1. Semantic search:
2. Klasifikasi teks:
3. Rekomendasi:
4. Deteksi anomali:

---

## 6. Keterbatasan

TODO: sebutkan minimal 3 keterbatasan, misalnya:

- model kecil punya keterbatasan bahasa/domain;
- cosine similarity tidak memahami negasi dan angka dengan sempurna;
- kualitas bergantung pada model dan chunking;
- embedding tidak menjamin fakta benar.

---

## 7. Refleksi

TODO: apa pelajaran utama minggu ini? Bagaimana konsep ini akan dipakai di RAG?
