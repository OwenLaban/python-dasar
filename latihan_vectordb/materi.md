# Materi Minggu 14 — Vector Database

> Tujuan: setelah membaca ini, kamu bisa menjelaskan apa itu vector database,
> kapan dibutuhkannya, bagaimana index dan metadata filter bekerja, dan
> bagaimana mengukur kualitas retrieval dengan benar.

---

## 1. Masalah: menyimpan banyak vektor

Minggu 13 kita mencari di antara 20 kalimat. Cara paling sederhana adalah
brute force: bandingkan query dengan **setiap** dokumen satu per satu.

```text
1 dokumen   → 1 perbandingan
100 dokumen → 100 perbandingan
1 juta      → 1 juta perbandingan
```

Untuk 100 dokumen ini masih cepat. Tapi dokumen bisa berjumlah jutaan, dan
perbandingan satu per satu sudah tidak masuk akal. Selain itu, setiap dokumen
real punya metadata (kategori, tanggal, sumber) yang harus bisa disaring.

**Vector database** menjawab dua masalah sekaligus:

1. menyimpan vektor + metadata secara persisten;
2. mencari tetangga terdekat dengan cepat lewat index.

---

## 2. Anatomi vector database

```text
┌─────────────┐   teks    ┌──────────────┐   vektor   ┌────────────────┐
│  Dokumen     │ ───────► │  Embedding    │ ─────────► │  Vector DB     │
│  (pdf, md)   │           │  service      │            │  index + store │
└─────────────┘           └──────────────┘            └────────┬───────┘
                                                                │ query vektor
                                                                ▼
                                                        ┌───────────────┐
                                                        │  Top-k dokumen │
                                                        └───────────────┘
```

Empat komponen yang selalu ada:

| Komponen | Isi | Contoh |
|---|---|---|
| Embedding service | Mengubah teks jadi vektor | Ollama + `bge-m3` |
| Index | Struktur data untuk pencarian cepat | HNSW, IVF |
| Store | Vektor, metadata, dokumen | File lokal, disk, RAM |
| Metadata | Atribut tambahan per dokumen | kategori, tahun, sumber |

---

## 3. Index: kenapa tidak brute force

**ANN (Approximate Nearest Neighbor)**/search approximate memakai index
untuk memperkecil jumlah perbandingan. Dua index yang paling umum:

### HNSW (Hierarchical Navigable Small World)

- Membangun **graf** antar titik vektor.
- Pencarian mulai dari titik acak, lalu melompat ke tetangga yang lebih dekat.
- Multi-level: lapisan atas jarak jauh, lapisan bawah jarak dekat.
- **Recall tinggi**, tetapi memakai RAM cukup banyak.

### IVF (Inverted File)

- Vektor dip partitioning ke beberapa *cluster* (misal dengan k-means).
- Query hanya dibandingkan dengan cluster yang paling mungkin berisi jawabannya.
- **Latency rendah**, recall bisa turun kalau cluster yang benar terlewat.

### Tradeoff yang harus dipahami

```text
HNSW  → recall tinggi, RAM besar, indexing lambat
IVF   → recall bisa turun, RAM kecil, query cepat
exact → recall 100%, tapi O(jumlah dokumen)
```

Tidak ada setting yang "benar" untuk semua kasus. Vector DB biasanya
menyediakan knob untuk menyeimbangkan: `hnsw:search_ef` (efektor Effort),
`nprobe` untuk IVF, `max_connections`, dan seterusnya.

> Untuk 100 dokumen, brute force **sama akuratnya** dengan index, dan sering
> kali lebih cepat karena tidak ada overhead. Index baru memberi Untung saat
> datanya besar. Jangan lupa mengukurnya, bukan berasumsi.

---

## 4. Metadata filter

Metadata adalah atribut penanda setiap dokumen. Contoh pada lab ini:

```json
{
  "kategori": "keuangan",
  "level": "dasar",
  "tahun": 2024,
  "tag": "keuangan, dasar"
}
```

Dua strategi filter:

- **Pre-filter**: saring dulu, baru cari yang mirip di antara hasil saringan.
- **Post-filter**: cari dulu top-k, lalu buang yang tidak cocok.

Pre-filter lebih tepat kalau hasil filter sedikit. Post-filter bisa gagal
memenuhi kuota: filter sangat selektif, sementara top-k diambil sebelum
penyaringan.

Chroma mendukung keduanya lewat operator:

```text
{"kategori": "keuangan"}                    # $eq
{"level": {"$in": ["dasar", "menengah"]}}     # $in
{"tahun": {"$gte": 2024}}                   # $gte, $lte, $gt, $lt
{"$and": [...]} / {"$or": [...]}             # gabungan
```

> Batasan penting Chroma: nilai metadata hanya boleh `str`, `int`, `float`,
> atau `bool`. **List tidak diterima** dan harus diubah jadi string.

---

## 5. Chroma API yang dipakai di lab

```python
import chromadb

client = chromadb.PersistentClient(path="./.chroma")
koleksi = client.get_or_create_collection(
    name="dokumen",
    metadata={"hnsw:space": "cosine"},
)

koleksi.add(
    ids=["dok-01"],
    documents=["Tidur cukup tujuh jam membantu tubuh pulih."],
    embeddings=[[0.12, -0.45, ...]],      # vektor dari Ollama
    metadatas=[{"kategori": "kesehatan"}],
)

hasil = koleksi.query(
    query_embeddings=[[0.31, 0.08, ...]],
    n_results=3,
    where={"kategori": "kesehatan"},      # opsional
    include=["documents", "metadatas", "distances"],
)
```

Hal yang perlu diingat:

- **Vektor dikirim sendiri.** Kalau `embeddings` tidak diisi, Chroma memakai
  model embedding bawaannya (butuh unduh model + internet). Kita sudah punya
  Ollama lokal, jadi vektor kita hitung sendiri.
- **ID unik dan stabil.** ID sama = dokumen diperbarui (upsert), bukan
  diduplikasi.
- **Ruang jarak.** `hnsw:space="cosine"` memakai jarak cosine
  (`jarak = 1 - cosine_similarity`). `"l2"` memakai jarak Euclidean,
  `"ip"` memakai inner product.
- **Persistent.** `PersistentClient` menyimpan ke folder, jadi data tetap ada
  setelah program ditutup. `EphemeralClient` hanya di RAM.

---

## 6. Memilih vector database

| Database | Cara jalan | Kelebihan | Kekurangan |
|---|---|---|---|
| **Chroma** | pip / embedded | Paling gampang, lokal, metadata filter | Opsi produksi terbatas |
| **Qdrant** | Docker / server | Cepat, filter kaya, REST API | Perlu Docker atau binary |
| **pgvector** | Ekstensi PostgreSQL | relational + vektor satu DB | Butuh PostgreSQL |
| **FAISS** | Library C++ | Sangat cepat, ringan | Tidak punya metadata/DB |
| **Milvus** | Server cluster | Skala besar, multi-tenant | Kompleks, berat resource |

Pertimbangan untuk mesin ini (RAM 7,7 GB, tanpa GPU):

- **Chroma embedded** paling ringan untuk 100–10 ribu dokumen.
- **Qdrant via Docker** menambah ~300 MB RAM untuk Chroma yang selalu hidup.
- **FAISS** paling cepat, tapi tanpa metadata — tidak cocok untuk lab yang
  memegang filter.
- Semua pilihan di atas bisa **gratis** dan **lokal**, jadi tidak ada API key
  yang bocor.

---

## 7. Mengukur kualitas retrieval

Setelah dapat hasil pencarian, jangan langsung percaya. Ukur:

| Metrik | Arti | Kapan dipakai |
|---|---|---|
| Precision@k | Berapa dari k hasil teratas yang relevan | Ada 1 jawaban benar |
| Recall@k | Berapa dari semua dokumen relevan yang ditemukan | Banyak jawaban benar |
| MRR | Posisi rata-rata dokumen pertama yang benar | Urutan penting |
| p95 latency | Latensi Worse case (95 persentil) | Batas waktu permintaan |

Precision yang dipakai di lab ini adalah **precision berbasis kategori**:
dokumen dianggap relevan bila `metadata.kategori` sama dengan kategori target
query. Metrik ini murah dan otomatis, tapi kasar — dokumen dari kategori lain
yang tetap menjawab pertanyaan akan dihitung salah. Sistem nyata perlu
penilaian manusia atau LLM-as-judge.

---

## 8. Praktik yang sering terlewat

1. **ID harus stabil.** ID dari hash isi dokumen (lihat `id_stabil()`) membuat
   index ulang aman: dokumen yang tidak berubah tidak diduplikasi.
2. **Update = re-embed.** Teks berubah berarti vektor harus dihitung ulang.
3. **Metadata dinormalisasi sebelum disimpan.** List harus jadi string, `None`
   harus dibuang — kalau tidak, Chroma menolak menyimpan.
4. **Chunking sebelum indexing.** Embedding satu dokumen panjang kehilangan
   detail. Potong menjadi beberapa chunk dengan overlap.
5. **Deduplikasi.** Dokumen yang sama dengan ID berbeda wasting space dan
   mengacaukan hasil pencarian.
6. **Hybrid search.** Gabungkan pencarian metadata (kata kunci/filter) dengan
   pencarian vektor untuk hasil terbaik.

---

## 9. Biaya dan batasan di mesin ini

| Komponen | Uso |
|---|---|
| `bge-m3` (embedding) | ± 1,2 GB RAM saat model aktif |
| Chroma embedded | ± 200–400 MB RAM |
| 100 dokumen × 1024 dim | ± 0,4 MB data vektor |

Angka vektor kecil. Yang mahal adalah **model embedding** dan **index HNSW**
untuk data besar. Untuk dataset kecil, brute force di RAM justru paling
irit.

---

## 10. Hubungan dengan RAG

```text
dokumen → chunk → embedding → vector DB
                             ↑
user → embedding → retrieve → top-k chunk → prompt → LLM → jawaban
```

Minggu 14 kita menyelesaikan bagian **vector DB**-nya. Minggu 15 merangkai
pipeline penuh, Minggu 16 membuat proyek tanya-jawab dokumen dengan sitasi.

Yang sudah ada di lab ini nanti akan dipakai ulang:

- `normalisasi_metadata()` → dipakai untuk filter dan pembagian metadata;
- `cari_semantik()` → substitusi retrieval saat vector DB belum siap;
- `EmbeddingClient` (Minggu 13) → sumber vektor.

---

## 11. Ringkasan

- Vector DB = penyimpanan vektor + index pencarian + metadata filter.
- Brute force akurat tapi O(n); index HNSW/IVF trades recall, RAM, dan latency.
- Metadata filter sering lebih penting daripada memilih model yang lebih besar.
- Chroma lokal gratis, tanpa API key, jalan embedded di laptop.
- Ukur retrieval dengan precision/recall dan latensi, bukan dengan perasaan.
- ID stabil, metadata bersih, dan re-embed saat update adalah kunci operasional.

Sekarang buka `vektor_db.py`, implementasikan fungsinya, lalu jalankan test.
