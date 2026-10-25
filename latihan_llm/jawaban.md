# Jawaban Lab Tokenizer — Minggu 7

Isi setelah menjalankan `python -m latihan_llm.tokenizer_lab`.

## 1. Hasil

- Token teks A: 9
- Token teks B: 11
- `kemerdekaan`: 3 token
- `ketidaksempurnaan`: 6 token
- `AI Engineer`: 2 token

## 2. Analisis

- Teks mana yang lebih banyak token? B
- Kenapa hasilnya bisa berbeda? karena B mempunyai lebih banyak kata dari A dan karena tiap kata berkemungkinan lebih dari 1 token maka teks dengan kata lebih banyak lebih memungkinkan untuk memiliki banyak token
- Apakah kesimpulan “bahasa Indonesia selalu lebih boros token” benar? tidak

## 3. Context window

- Apakah 8.000 token sama dengan 8.000 kata? tidak
- Kira-kira 8.000 token setara berapa kata? sekitar 6.000–6.500 kata untuk contoh teks ini (kurang dari 8.000 kata)
- Kenapa context window dihitung dalam token, bukan kata? karena model memproses teks sebagai urutan token; biaya, context window, dan komputasi dihitung berdasarkan token

## 4. Kesimpulan pribadi

kemampuan ai tidak sama dengan manusia untuk memproses sesuatu, jadi hasil dan prosesnya juga berbeda
