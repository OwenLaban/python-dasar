# Laporan Eksperimen Embedding — Minggu 13

Tanggal: 01/11/2026
Model: `nomic-embed-text`
Dimensi: 768
Hardware: Intel Core i7-1195G7, RAM 7,7 GB, NVIDIA MX450 2 GB VRAM
Ollama: 0.40.13

---

## 1. Pertanyaan

Apakah embedding bisa menemukan kalimat yang **maknanya relevan** meskipun
kata-katanya tidak sama persis dengan query?

Pertanyaan turunan:

- Seberapa sering hasil teratas sesuai topik?
- Kapan cosine similarity menyesatkan?
- Apakah bahasa query memengaruhi kualitas retrieval?

---

## 2. Metode

- 20 kalimat dari 4 topik: teknologi, kuliner, olahraga, dan keuangan
  (5 kalimat per topik).
- 4 query, masing-masing punya topik target.
- Setiap teks diubah menjadi vektor 768 dimensi dengan `nomic-embed-text`
  lewat Ollama.
- Vektor dinormalisasi, lalu diurutkan dengan cosine similarity.
- Metrik: top-1 relevan dan **precision@3**, yaitu proporsi 3 hasil teratas
  yang topiknya sesuai.
- Waktu embedding 24 teks (20 kalimat + 4 query): **9,12 detik**.
- Uji tambahan: query keuangan diterjemahkan ke bahasa Inggris untuk melihat
  pengaruh bahasa query.

Perintah reproduksi:

```powershell
.\.venv\Scripts\python.exe -m latihan_embedding.eksperimen_embedding
.\.venv\Scripts\python.exe -m latihan_embedding.uji_bahasa
```

---

## 3. Hasil

| # | Query | Top-1 | Skor | Relevan? | Precision@3 |
|---|---|---|---|---|---|
| 1 | bagaimana memulai karier sebagai programmer | Python (teknologi) | 0,7129 | ya | 1,00 |
| 2 | makanan hangat berkuah untuk makan siang | Bakso (kuliner) | 0,7472 | ya | 0,33 |
| 3 | olahraga ringan yang aman untuk pemula | Pemanasan (olahraga) | 0,7212 | ya | 0,67 |
| 4 | cara mengelola uang agar tidak cepat habis | Docker (teknologi) | 0,7363 | tidak | 0,00 |

Top-3 lengkap:

```text
Query 1: bagaimana memulai karier sebagai programmer (target: teknologi)
  1. [0,7129] teknologi  Python adalah bahasa pemrograman yang populer untuk membangun aplikasi web.
  2. [0,7081] teknologi  API memungkinkan dua program saling bertukar data.
  3. [0,6701] teknologi  Docker membantu mengemas aplikasi agar berjalan sama di berbagai komputer.
  precision@3: 1,00

Query 2: makanan hangat berkuah untuk makan siang (target: kuliner)
  1. [0,7472] kuliner   Bakso disajikan dengan kuah kaldu hangat dan mie kuning.
  2. [0,6555] keuangan  Anggaran bulanan membantu mengendalikan pengeluaran rumah tangga.
  3. [0,6439] keuangan  Asuransi kesehatan membantu menutup biaya pengobatan yang mahal.
  precision@3: 0,33

Query 3: olahraga ringan yang aman untuk pemula (target: olahraga)
  1. [0,7212] olahraga  Pemanasan sebelum olahraga mengurangi risiko cedera otot.
  2. [0,6639] olahraga  Renang melatih hampir seluruh otot tubuh tanpa membebani sendi.
  3. [0,6635] keuangan  Asuransi kesehatan membantu menutup biaya pengobatan yang mahal.
  precision@3: 0,67

Query 4: cara mengelola uang agar tidak cepat habis (target: keuangan)
  1. [0,7363] teknologi  Docker membantu mengemas aplikasi agar berjalan sama di berbagai komputer.
  2. [0,7016] olahraga   Pemanasan sebelum olahraga mengurangi risiko cedera otot.
  3. [0,6981] olahraga   Tim sepak bola itu menang melalui gol di menit akhir.
  precision@3: 0,00
```

Catatan penting: **skor tertinggi bukan berarti paling relevan.** Docker
mendapat 0,7363 untuk query yang salah, lebih tinggi daripada Python (0,7129)
untuk query yang benar. Cosine similarity tidak punya ambang batas universal.

---

## 4. Analisis

### 1. Query mana yang paling berhasil? Mengapa?

Query 1, dengan precision@3 = 1,00. Ketiga hasil teratas semuanya bertopik
teknologi, dan top-1 adalah kalimat tentang Python (0,7129), lalu API (0,7081)
dan Docker (0,6701). Query memakai kata `programmer`, yang dekat dengan
`pemrograman` dan `aplikasi web` di kalimat teratas. Artinya, retrieval bekerja
baik ketika kosakata query dan dokumen berada di domain yang sama.

### 2. Query mana yang hasilnya mengejutkan atau meleset?

Query 4 paling meleset: precision@3 = 0,00. Ketiga hasilnya bukan tentang
keuangan sama sekali, dan top-1 justru Docker (0,7363). Query 2 juga hanya
mendapat 0,33: setelah Bakso di posisi 1, dua hasil berikutnya justru tentang
keuangan. Query 3 mendapat 0,67 karena dua hasil olahraga diikuti Asuransi
kesehatan di posisi 3.

### 3. Apakah ada kalimat yang mirip secara kata tetapi berbeda makna?

Ada indikasi. Pada query 3, `Asuransi kesehatan...` muncul di posisi 3. Kata
`aman` pada query dan `asuransi` pada dokumen berbagi bentuk huruf, tetapi
topiknya berbeda. Ini bisa jadi kemiripan permukaan, bukan kemiripan makna.
Query 2 juga memunculkan dua kalimat keuangan yang sulit dijelaskan secara
semantik dari kata `makanan hangat berkuah`. Model kecil dan teks di luar
bahasa latihannya membuat skor tidak selalu bisa dijelaskan oleh manusia.

### 4. Apakah cosine similarity cukup untuk menilai relevansi? Apa yang hilang?

Tidak cukup. Cosine hanya mengukur kedekatan **relatif** antara dua vektor,
bukan kebenaran, maksud pengguna, atau kualitas jawaban. Buktinya, hasil yang
salah (Docker, 0,7363) bisa lebih tinggi daripada hasil yang benar (Python,
0,7129). Yang hilang antara lain:

- pemahaman negasi (`berhasil` vs `tidak berhasil`);
- angka dan entitas unik (`25 MW` vs `52 MW`, `PT A` vs `PT B`);
- maksud query dan konteks percakapan;
- penilaian apakah isi kalimat faktual atau sudah usang;
- kalibrasi skor antar-query dan antar-bahasa.

Karena itu, cosine sebaiknya dipakai untuk **ranking**, lalu hasil top-k
diperiksa manusia, diberi reranker, atau dinilai dengan LLM-as-judge.

### 5. Kata kunci vs embedding

| Aspek | Pencarian kata kunci | Embedding |
|---|---|---|
| Sinonim | Sering gagal | Bisa menangkap, jika bahasa cocok |
| Nama/angka unik | Presisi tinggi | Bisa tertukar |
| Salah ejaan | Sering gagal | Lebih toleran |
| Penjelasan | Mudah diaudit | Sulit dijelaskan |
| Kecepatan | Sangat cepat | Perlu hitung vektor |

Pada data ini, kata kunci `mengelola uang` tidak akan menemukan satu kalimat
pun karena tidak ada kalimat yang memuat kata `uang` secara persis. Embedding
seharusnya menutup celah itu, tetapi justru gagal dalam bahasa Indonesia.
Setelah query diterjemahkan ke bahasa Inggris, hasilnya membaik. Jadi solusi
nyatanya bukan hanya **hybrid search** (kata kunci + embedding), tetapi juga
model multibahasa atau terjemahan query, ditambah reranking.

### Uji tambahan: pengaruh bahasa query

Uji dijalankan 02/11/2026 dengan 20 kalimat yang sama.

| Query | Top-1 | Skor | Precision@3 |
|---|---|---|---|
| ID: cara mengelola uang agar tidak cepat habis | Docker (teknologi) | 0,7363 | 0,00 |
| EN: how to manage money so it does not run out quickly | Investasi saham (keuangan) | 0,4908 | 0,67 |
| ID: mengelola uang | Tim sepak bola (olahraga) | 0,6602 | 0,33 |
| EN: manage money | Investasi saham (keuangan) | 0,4970 | 0,67 |

Terjemahan ke bahasa Inggris menaikkan precision@3 dari 0,00 menjadi 0,67
untuk query lengkap, dan dari 0,33 menjadi 0,67 untuk query pendek. Ini
mendukung dugaan bahwa `nomic-embed-text` lebih kuat pada bahasa Inggris
daripada bahasa Indonesia.

Namun, skor hasil yang benar justru **lebih rendah** (0,4908) daripada skor
hasil yang salah dalam bahasa Indonesia (0,7363). Ini menegaskan lagi bahwa
angka cosine tidak bisa dibandingkan antar-query. Uji ini juga hanya memakai
satu topik dan satu query, jadi hasilnya tidak boleh digeneralisasi ke semua
kasus.

---

## 5. Use Case

1. **Semantic search.** Pencarian SOP atau knowledge base internal. Karyawan
   mengetik "cara ajukan cuti", sistem menemukan dokumen "prosedur permohonan
   libur" meskipun kata-katanya berbeda. Untuk teks Indonesia, model harus
   multibahasa atau query diterjemahkan lebih dulu.
2. **Klasifikasi teks.** Embedding email atau tiket keluhan, lalu beri label
   spam/bukan spam atau rutekan ke tim yang tepat. Contoh: keluhan "barang
   rusak" dan "paket penyok" masuk ke tim pengembalian barang meskipun
   kalimatnya berbeda.
3. **Rekomendasi.** Embed artikel, produk, atau lagu, lalu rekomendasikan item
   yang vektornya dekat dengan item yang disukai pengguna. Contoh: fitur
   "artikel terkait" di blog atau "produk serupa" di toko online.
4. **Deteksi anomali.** Teks yang jauh dari kelompok normal bisa menandakan
   hal tidak biasa. Contoh: pesan log error yang belum pernah muncul, atau
   komentar yang topiknya menyimpang jauh dari biasanya. Ambang batasnya
   harus ditentukan dari distribusi data, bukan angka cosine absolut.

---

## 6. Keterbatasan

1. **Bahasa dan domain.** `nomic-embed-text` dilatih terutama untuk bahasa
   Inggris. Query keuangan berbahasa Indonesia gagal total, sedangkan versi
   Inggrisnya mendapat precision@3 = 0,67.
2. **Skor tidak terkalibrasi.** Tidak ada ambang cosine universal. Hasil salah
   bisa mendapat 0,7363, lebih tinggi daripada hasil benar (0,7129). Perbandingan
   skor hanya bermakna di dalam satu query yang sama.
3. **Negasi, angka, dan nama unik.** `berhasil` dan `tidak berhasil`, atau
   `25 MW` dan `52 MW`, bisa menghasilkan vektor yang dekat. Model kecil juga
   bisa tertukar membedakan nama perusahaan atau produk.
4. **Satu vektor untuk teks panjang.** Paragraf panjang yang diubah menjadi
   satu vektor kehilangan detail. RAG perlu chunking dengan overlap agar
   informasi tidak hilang.
5. **Mirip bukan berarti benar.** Embedding tidak memverifikasi fakta. Dua
   dokumen bisa sangat mirip tetapi salah satunya sudah usang atau keliru.
6. **Metrik topik terlalu kasar.** Precision@3 berdasarkan topik bisa
   menilai kalimat keuangan sebagai relevan meskipun tidak menjawab pertanyaan
   tentang cara mengelola uang. Sebaliknya, jawaban relevan dari topik lain
   bisa dihitung salah.
7. **Belum ada reranking.** Lab ini hanya mengurutkan dengan cosine. Sistem
   nyata biasanya menambahkan reranker atau LLM-as-judge untuk memperbaiki
   urutan teratas.

---

## 7. Refleksi

Pelajaran utama minggu ini: **kualitas retrieval sangat bergantung pada
kecocokan model dengan bahasa dan domain data.** Matematika cosine sudah
benar, normalisasi sudah benar, tetapi query keuangan tetap gagal karena model
lebih mengenal bahasa Inggris. Menerjemahkan query memperbaiki hasil, jadi
masalahnya bukan pada rumus, melainkan pada representasi.

Kedua, cosine similarity adalah alat **ranking**, bukan alat kebenaran. Skor
0,7363 bisa saja milik hasil yang salah. Karena itu, evaluasi tidak boleh
hanya melihat rata-rata skor; kita perlu memeriksa top-k per query, menghitung
precision/recall, dan menambahkan penilaian manusia atau LLM.

Untuk RAG di Minggu 15–16, konsep ini akan dipakai untuk mengambil chunk
dokumen yang relevan sebelum dikirim ke LLM. Agar tidak mengulang kegagalan
minggu ini, saya perlu:

- memilih model embedding multibahasa (misalnya `bge-m3`) atau menerjemahkan
  query;
- memotong dokumen menjadi chunk dengan overlap;
- menyimpan vektor di vector database (Minggu 14);
- menggabungkan pencarian kata kunci dan embedding (hybrid search);
- menambahkan reranking serta evaluasi retrieval terpisah dari kualitas
  jawaban LLM.

Embedding tidak menjamin jawaban benar. Ia hanya membantu menemukan kandidat
yang relevan; kebenaran akhir tetap harus diperiksa dari sumbernya.
