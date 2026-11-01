# Materi Minggu 13 — Embeddings

> Tujuan: setelah membaca ini, kamu bisa menjelaskan apa itu embedding,
> mengapa ia berguna, cara mengukur kemiripan, dan kapan metodenya gagal.

---

## 1. Masalah: komputer tidak memahami makna

Pencarian kata kunci biasa mencocokkan **teks yang sama**. Contoh:

- Query: `mobil murah`
- Dokumen: `kendaraan roda empat dengan harga terjangkau`

Tidak ada kata `mobil` atau `murah` di dokumen, sehingga pencarian kata kunci
bisa melewatkannya. Manusia tahu kedua kalimat itu membahas hal yang mirip,
tetapi komputer tidak.

**Embedding** mengubah teks menjadi daftar angka (vektor) sedemikian rupa
sehingga teks dengan makna mirip menghasilkan vektor yang berdekatan.

```text
"mobil murah"        → [0.12, -0.45, 0.88, ...]  (768 angka)
"kendaraan ekonomis" → [0.10, -0.41, 0.85, ...]  (768 angka)
"resep rendang"      → [-0.77, 0.22, 0.03, ...]  (768 angka)
```

Dua vektor pertama berdekatan; vektor ketiga jauh.

---

## 2. Dari teks ke vektor

Secara sederhana:

```text
teks → tokenizer → model neural network → pooling → vektor
```

1. Teks dipecah menjadi token.
2. Model (mis. transformer) memproses token dan konteks sekitarnya.
3. Hasilnya diringkas menjadi satu vektor tetap, misalnya 384, 768, atau 1536
   dimensi.
4. Vektor itu disimpan atau dibandingkan dengan vektor lain.

Embedding **bukan** jawaban model dan bukan database. Ia hanya representasi
angka dari makna sebuah teks.

### Istilah penting

| Istilah | Arti |
|---|---|
| Dimensi | Jumlah angka dalam satu vektor (mis. 768) |
| Vector space | Ruang tempat semua vektor berada |
| Similarity | Ukuran kedekatan dua vektor |
| Normalisasi | Membuat panjang vektor menjadi 1 |
| Query | Teks yang dicari |
| Kandidat | Teks yang dibandingkan dengan query |

---

## 3. Cosine similarity

Rumus yang paling umum untuk membandingkan embedding:

```text
cosine_similarity(a, b) = (a · b) / (||a|| × ||b||)
```

- `a · b` = dot product: kalikan elemen yang sama, lalu jumlahkan.
- `||a||` = panjang vektor: akar dari jumlah kuadrat elemen.
- Hasilnya berada di rentang **-1 sampai 1**:
  - `1` → arah sama (sangat mirip),
  - `0` → tegak lurus (tidak terkait),
  - `-1` → arah berlawanan.

Contoh:

```text
a = [1, 0]
b = [0.8, 0.6]

a · b = 1×0.8 + 0×0.6 = 0.8
||a|| = 1
||b|| = sqrt(0.8² + 0.6²) = 1
cosine = 0.8 / (1 × 1) = 0.8
```

### Mengapa cosine, bukan jarak Euclidean?

Cosine hanya peduli pada **arah**, bukan panjang vektor. Untuk embedding teks,
arah biasanya lebih penting daripada besarnya. Dua teks yang mirip bisa
menghasilkan vektor dengan panjang berbeda; cosine tetap menilainya mirip.

### Normalisasi

Jika semua vektor sudah dinormalisasi (panjang 1), maka:

```text
cosine_similarity(a, b) = dot_product(a, b)
```

Karena itu banyak sistem menormalisasi vektor sekali di awal, lalu memakai dot
product yang lebih murah. Di lab ini kita tetap menghitung cosine secara
eksplisit agar rumusnya terlihat.

---

## 4. Semantic search

Alur pencarian semantik:

```text
1. Siapkan dokumen.
2. Ubah setiap dokumen menjadi vektor → simpan.
3. Ubah query menjadi vektor.
4. Hitung similarity(query, semua dokumen).
5. Urutkan menurun, ambil top-k.
```

Contoh hasil:

```text
Query: "olahraga ringan yang aman untuk pemula"
1. [0.71] (olahraga) Renang melatih hampir seluruh otot tanpa membebani sendi.
2. [0.68] (olahraga) Jogging pagi membantu menjaga kebugaran jantung.
3. [0.61] (olahraga) Pemanasan sebelum olahraga mengurangi risiko cedera.
```

Perhatikan bahwa query tidak memakai kata `renang`, `jogging`, atau `pemanasan`.
Model menangkap bahwa semuanya masih berkaitan dengan olahraga ringan.

### Evaluasi sederhana

**Precision@k** = jumlah hasil relevan di top-k dibagi jumlah hasil yang
diperiksa.

```text
top-3 = [teknologi, kuliner, teknologi]
precision@3 untuk topik teknologi = 2/3 = 0.67
```

Metrik ini sederhana dan bisa menipu jika topiknya tidak jelas. Untuk sistem
nyata, kita juga perlu penilaian manusia atau LLM-as-judge.

---

## 5. Empat use case utama

### 1. Semantic search

Mencari dokumen, FAQ, atau produk berdasarkan makna query.

Contoh: pencarian di knowledge base perusahaan, meskipun karyawan memakai
istilah yang berbeda dari dokumen.

### 2. Klasifikasi teks

Vektor teks bisa menjadi input classifier:

```text
embedding(email) → classifier → spam / bukan spam
```

Atau tanpa training: bandingkan dengan embedding contoh tiap kelas
(*few-shot classification*).

### 3. Rekomendasi

Barang, artikel, atau lagu yang mirip dengan yang disukai pengguna.

```text
embedding(item yang disukai) ≈ embedding(item rekomendasi)
```

### 4. Deteksi anomali

Teks yang jauh dari kelompok normal bisa menandakan hal tidak biasa:

- komentar yang sangat menyimpang dari topik;
- log error yang tidak pernah muncul sebelumnya;
- transaksi atau dokumen dengan pola berbeda.

---

## 6. Memilih model embedding

| Model | Dimensi | Ukuran/akses | Catatan |
|---|---:|---|---|
| `text-embedding-3-small` (OpenAI) | 1536 | API berbayar | Kualitas baik, butuh API key, data keluar |
| `all-MiniLM-L6-v2` (Sentence Transformers) | 384 | ~90 MB, lokal | Ringan, butuh PyTorch |
| `nomic-embed-text` (Ollama) | 768 | ~274 MB, lokal | Dipakai lab ini, tanpa PyTorch |
| `bge-m3` | 1024 | ~2 GB, lokal | Multibahasa, lebih berat |
| `mxbai-embed-large` | 1024 | ~670 MB, lokal | Kualitas baik, lebih berat |

Pertimbangan:

- **Bahasa**: pastikan model mendukung bahasa Indonesia dengan baik.
- **Dimensi**: lebih besar belum tentu lebih baik; butuh memori dan waktu.
- **Hardware**: model 274 MB jauh lebih ramah daripada model 2 GB.
- **Privasi**: API pihak ketiga berarti data keluar dari komputer.
- **Biaya**: API berbayar vs listrik dan waktu untuk model lokal.
- **Domain**: model umum bisa kurang tepat untuk hukum, medis, atau kode.

---

## 7. Embedding vs pencarian kata kunci

| Aspek | Kata kunci | Embedding |
|---|---|---|
| Cocok dengan sinonim | Tidak | Ya |
| Salah ejaan | Sering gagal | Lebih toleran |
| Negasi | Bisa salah | Bisa salah juga |
| Nama/angka unik | Presisi tinggi | Bisa tertukar |
| Kecepatan | Sangat cepat | Perlu hitung vektor |
| Penjelasan | Mudah | Sulit dijelaskan |

Sering kali sistem terbaik menggabungkan keduanya (**hybrid search**):
cari dengan kata kunci dan embedding, lalu gabungkan skornya.

---

## 8. Keterbatasan yang wajib diingat

1. **Mirip ≠ benar.** Dua kalimat bisa mirip secara makna tetapi satu berisi
   fakta yang salah.
2. **Negasi.** `"proyek berhasil"` dan `"proyek tidak berhasil"` bisa punya
   embedding yang dekat karena kata-katanya hampir sama.
3. **Angka dan nama.** `25 MW` vs `52 MW`, atau `PT A` vs `PT B`, bisa sulit
   dibedakan oleh model kecil.
4. **Panjang teks.** Satu vektor untuk paragraf panjang kehilangan detail.
   Karena itu RAG memakai chunking.
5. **Domain shift.** Model yang dilatih pada teks umum bisa lemah pada istilah
   medis/hukum.
6. **Bias dan bahasa.** Kualitas berbeda antar bahasa dan kelompok.
7. **Biaya tersembunyi.** Menghitung embedding untuk jutaan dokumen butuh
   waktu, memori, dan penyimpanan.

---

## 9. Hubungan dengan RAG

RAG (Retrieval-Augmented Generation) memakai embedding untuk menemukan potongan
dokumen yang relevan, lalu mengirim potongan itu ke LLM.

```text
pertanyaan → embedding → cari chunk relevan → prompt + chunk → LLM → jawaban
```

Minggu ini kita membangun fondasinya:

- Minggu 13: mengubah teks menjadi vektor dan mencari yang mirip.
- Minggu 14: menyimpan vektor di vector database.
- Minggu 15: merangkai pipeline retrieval + generation.
- Minggu 16: proyek RAG dengan sitasi.

---

## 10. Ringkasan

- Embedding = teks menjadi vektor makna.
- Makna mirip → vektor berdekatan.
- Cosine similarity mengukur arah, bukan panjang.
- Normalisasi membuat dot product setara dengan cosine.
- Semantic search = embed query, bandingkan dengan semua kandidat, ambil top-k.
- Embedding kuat untuk sinonim, tetapi bukan jaminan kebenaran.
- Metrik sederhana seperti precision@k membantu, tetapi tidak cukup sendirian.

Sekarang buka `vektor.py`, implementasikan fungsinya, lalu jalankan test.
