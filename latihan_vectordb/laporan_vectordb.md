# Laporan Eksperimen Vector Database — Minggu 14

Tanggal: TODO
Model embedding: TODO
Dimensi: TODO
Chroma: TODO (versi)
Ollama: TODO (versi)
Hardware: Intel Core i7-1195G7, RAM 7,7 GB, NVIDIA MX450 2 GB VRAM

---

## 1. Pertanyaan

Apakah vector database membuat pencarian semantik **lebih cepat dan lebih
berguna** dibandingkan membandingkan vektor satu per satu — dan apakah
metadata filter membuat hasil jauh lebih relevan?

---

## 2. Metode

- 100 dokumen berbahasa Indonesia, 5 kategori × 20 kalimat.
- Metadata per dokumen: `kategori`, `level` (dasar/menengah/lanjut), `tahun`,
  dan `tag`.
- 6 query semantic, masing-masing punya kategori target.
- Dua cara pencarian dibandingkan:
  - **naive** — `cari_semantik()` buatan sendiri (brute force di memori);
  - **Chroma** — index HNSW dengan `hnsw:space="cosine"`.
- Metrik: precision@3 berbasis kategori, latensi rata-rata per query,
  jumlah dokumen ter-index, dan waktu indexing.

---

## 3. Hasil

| Query | Kategori target | Presisi@3 naive | Presisi@3 Chroma | Latensi naive (ms) | Latensi Chroma (ms) |
|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO | TODO |

Waktu embedding: TODO s
Waktu indexing 100 dokumen: TODO s
Rata-rata precision@3: naive TODO | Chroma TODO

Top-3 per query (Chroma):

```text
TODO: tempel output eksperimen di sini
```

---

## 4. Analisis

TODO: jawab pertanyaan berikut.

1. Apakah hasil naive dan Chroma sama? Kalau berbeda, kenapa?
2. Chroma lebih cepat atau lambat di sini? Apakah itu sesuai harapanmu
   sebelum menjalankan?
3. Query mana yang gagal? Apa penyebabnya — model, data, atau metrik?
4. Apa keuntungan metadata filter dibanding semantic search murni?
5. Kapan vector database sebenarnya dibutuhkan, dan kapan brute force atau
   pencarian kata kunci cukup?

---

## 5. Metadata Filter dan CRUD

| Filter | Jumlah hasil | Kategori yang muncul |
|---|---|---|
| TODO | TODO | TODO |
| TODO | TODO | TODO |
| TODO | TODO | TODO |

Operasi data:

| Operasi | Jumlah dokumen |
|---|---|
| Awal | TODO |
| Setelah perbarui (upsert `keu-01`) | TODO |
| Setelah hapus `keu-02` | TODO |
| Setelah tambah ulang `keu-02` | TODO |

TODO: jelaskan apa yang terjadi pada tiap operasi dan mengapa.

---

## 6. Use Case

TODO: jelaskan minimal 3 kapan perlu vector database, dan berikan contoh nyata.

1. Knowledge base internal:
2. Katalog produk:
3. Arsip dokumen legal:

---

## 7. Keterbatasan

TODO: sebutkan minimal 3 keterbatasan, misalnya:

- index HNSW memakai RAM jauh lebih besar daripada data vektornya;
- metadata filter hanya sekuat skema metadata yang kita desain;
- model embedding tetap punya kelemahan pada sebagian bahasa;
- precision berbasis kategori terlalu kasar;
- satu proses Chroma tidak cocok untuk banyak pengguna.

---

## 8. Refleksi

TODO: apa pelajaran utama minggu ini? Bagaimana vector database dipakai di
pipeline RAG Minggu 15–16?
