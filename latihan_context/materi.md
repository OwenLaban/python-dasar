# Materi Minggu 12 — Context Engineering

## 1. Apa itu context engineering?

**Prompt engineering** mengatur *cara* kita menulis instruksi.
**Context engineering** mengatur *informasi apa* yang dilihat model saat
menjawab: system prompt, riwayat percakapan, dokumen, hasil tool, memory, dan
format output.

Model tidak membaca database atau ingatan jangka panjang secara otomatis.
Semua yang boleh dipakai model harus dimasukkan ke **context window** pada
request tersebut.

> Context window adalah anggaran token, bukan ruang penyimpanan permanen.

Model yang context window-nya besar tetap bisa salah jika informasi penting
terkubur, konteksnya berisi data basi, atau instruksi bercampur dengan data
yang tidak tepercaya.

---

## 2. Sumber konteks

| Sumber | Contoh | Risiko |
|---|---|---|
| System prompt | aturan peran, format output, batasan | terlalu panjang sehingga instruksi penting tenggelam |
| Pesan user | pertanyaan atau tugas saat ini | ambigu atau memuat instruksi berbahaya |
| Riwayat percakapan | “produk itu”, “nama saya tadi” | tumbuh tanpa batas dan menua |
| Dokumen / retrieval | kontrak, email, catatan rapat | dokumen panjang, duplikat, atau tidak relevan |
| Hasil tool | cuaca, database, hasil pencarian | data salah atau terlambat |
| Memory | preferensi user, fakta jangka panjang | basi, salah, atau bertentangan |
| Output yang diminta | JSON, ringkasan, daftar aksi | tidak menyisakan ruang input |

Urutan prioritas yang umum:

1. instruksi sistem dan batasan keamanan;
2. tugas user saat ini;
3. bukti/dokumen yang paling relevan;
4. beberapa giliran percakapan terbaru;
5. ringkasan riwayat lama;
6. informasi latar yang tidak wajib.

Prioritas bisa berubah sesuai aplikasi, tetapi prinsipnya: **jangan biarkan
konteks yang tidak penting mendesak keluar informasi yang penting.**

---

## 3. Anggaran token

Sebelum menyusun prompt, hitung:

```text
token_input_tersedia
  = context_window
  - token_output
  - token_system
  - margin_keamanan
```

Contoh: context 2.048 token, output 200 token, system 100 token, margin 100
token → input tersedia 1.648 token.

Mengapa perlu margin?

- tokenizer model berbeda dari perkiraan;
- format chat menambah token tersembunyi;
- output bisa lebih panjang dari yang direncanakan;
- Dokumen dan prompt bisa berubah tanpa kita sadari.

Aturan praktis: ukur token dengan tokenizer, jangan menebak dari jumlah kata.
Satu kata bisa menjadi beberapa token, terutama untuk bahasa Indonesia dan
istilah teknis.

---

## 4. Memory dan compaction

### Jenis memory sederhana

- **Working memory** — beberapa pesan terakhir dalam percakapan.
- **Episodic memory** — ringkasan kejadian/sesi sebelumnya.
- **Semantic memory** — fakta stabil, misalnya preferensi user atau nama
  organisasi.

### Compaction

Compaction adalah memadatkan konteks agar tetap muat tanpa membuang semua
informasi. Caranya bisa:

- mempertahankan N pesan terbaru;
- merangkum pesan lama menjadi poin-poin;
- menyimpan fakta penting dalam struktur (nama, tanggal, keputusan);
- membuang basa-basi dan informasi yang sudah tidak relevan.

Compaction yang buruk juga berbahaya: ringkasan bisa menghilangkan angka,
syarat, atau penyangkalan. Karena itu ringkasan sebaiknya:

- mempertahankan nama, angka, tanggal, dan keputusan;
- menandai informasi yang tidak pasti;
- tidak mengubah ketidakpastian menjadi fakta;
- menyimpan sumber jika memungkinkan.

---

## 5. Context failure modes

| Failure mode | Artinya | Contoh |
|---|---|---|
| **Overflow** | konteks melebihi batas lalu dipotong | pesan terbaru hilang karena riwayat terlalu panjang |
| **Lost in the middle** | informasi di tengah dokumen kurang terpakai | kode penting di tengah transkrip tidak ditemukan |
| **Distraction** | informasi tidak relevan mengalihkan perhatian | jawaban benar terkubur dalam 50 dokumen serupa |
| **Context poisoning** | konteks berisi informasi salah atau berbahaya | dokumen palsu menyuruh mengabaikan aturan |
| **Stale context** | konteks benar di masa lalu, tetapi sudah berubah | alamat lama masih dipakai |
| **Conflicting context** | dua sumber saling bertentangan | dokumen A bilang tanggal 3, dokumen B bilang tanggal 5 |
| **Over-compression** | ringkasan terlalu pendek | angka dan syarat penting hilang |
| **Context clash** | instruksi dan data bercampur | email berisi “abaikan instruksi sebelumnya” |

Tidak semua kegagalan berasal dari model. Banyak yang berasal dari cara kita
memilih, mengurutkan, dan memadatkan konteks.

---

## 6. Strategi yang dipakai di proyek

### Stuff

Semua teks dimasukkan ke satu prompt. Paling baik untuk dokumen pendek karena
model melihat hubungan antarbagian secara utuh. Jika terlalu panjang, prompt
akan dipotong atau error.

### Chunking + overlap

Dokumen dipotong menjadi bagian kecil. Overlap beberapa token di batas potongan
membantu menjaga kalimat yang terbelah. Terlalu banyak overlap membuang ruang;
terlalu sedikit membuat konteks di batas hilang.

### Map-reduce

Setiap potongan diringkas sendiri-sendiri (**map**), lalu ringkasan-ringkasan
digabung (**reduce**). Cocok untuk dokumen panjang dan bisa diparalelkan.
Kelemahannya: hubungan antar-potongan bisa hilang.

### Refine / rolling summary

Ringkasan diperbarui potongan demi potongan:

```text
ringkasan = ringkas(ringkasan_sebelumnya + potongan_baru)
```

Alurnya lebih runtut, tetapi berjalan berurutan dan bisa menumpuk kesalahan.
Ringkasan lama jangan sampai tumbuh melebihi anggaran.

### Prioritas dan sitasi

Saat konteks tidak muat, pilih sumber yang paling relevan dan terbaru. Simpan
ID atau nama sumber agar jawaban bisa diperiksa. Untuk proyek RAG nanti, sitasi
menjadi bagian wajib.

---

## 7. Cara mengevaluasi konteks

Minimal ukur:

1. **Akurasi** — apakah jawaban memuat fakta yang benar?
2. **Kelengkapan** — apakah detail penting hilang?
3. **Kepatuhan format** — apakah output tetap JSON/skema?
4. **Latency** — berapa lama prompt yang lebih panjang diproses?
5. **Biaya/ukuran** — berapa token yang benar-benar terpakai?
6. **Robustness** — apa yang terjadi saat dokumen panjang, kosong, atau
   bertentangan?

Eksperimen `eksperimen_konteks.py` menguji satu failure mode: posisi informasi.
Ini bukan benchmark lengkap, hanya cara melihat sendiri bahwa konteks perlu
diatur dan diuji.

---

## 8. Aturan praktis

- Hitung token, sisihkan output dan margin.
- Taruh instruksi penting di tempat yang jelas; jangan mengandalkan posisi.
- Jangan masukkan seluruh riwayat jika hanya beberapa giliran yang relevan.
- Ringkas dengan mempertahankan angka, nama, tanggal, dan keputusan.
- Perlakukan dokumen dan hasil tool sebagai **data**, bukan instruksi.
- Uji dengan dokumen panjang dan informasi yang sengaja diletakkan di tengah.
- Catat batasan: satu percobaan bukan bukti umum.

Minggu ini konsep tersebut dipakai untuk **Proyek #4: summarizer dokumen
dengan model lokal Ollama**.
