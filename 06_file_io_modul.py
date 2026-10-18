# ============================================
# LATIHAN 6: File I/O + Modul
# ============================================
# Cara pakai: isi bagian yang masih kosong, lalu jalankan:
#   python 06_file_io_modul.py
# Target: bisa menulis, membaca, dan menambah isi file teks dari Python.
# Catatan: latihan ini membuat file `latihan.txt` di folder yang sama.
# ============================================

# --- Konsep cepat ---
# open(nama_file, mode) = membuka file. Mode yang penting:
#   "r" -> read   (baca; ini default; error kalau file tidak ada)
#   "w" -> write  (tulis dari nol — ISI LAMA TERHAPUS!)
#   "a" -> append (tambah di akhir — isi lama aman)
#
# Cara paling aman memakai `with` — file otomatis ditutup setelah blok:
#   with open("latihan.txt", "w") as f:
#       f.write("baris pertama\n")   # \n = pindah baris
#
# Modul = kumpulan kode siap pakai yang di-import:
#   import math                -> math.sqrt(144) = 12.0
#   from datetime import date  -> date.today() = tanggal hari ini
# Praktik: letakkan semua `import` di bagian paling atas file.


# --- SOAL 1: tulis file dari nol ---
# TODO: dengan `with open("latihan.txt", "w") as f:`, tulis 3 nama
# makanan favoritmu, satu per baris (jangan lupa \n di tiap baris).
# Jalankan, lalu cek file `latihan.txt` muncul di folder ini.
# Pertanyaan (jawab di catatanmu): kalau programnya dijalankan DUA kali,
# isi file bertambah atau tertimpa? Kenapa?


# --- SOAL 2: baca seluruh isi ---
# TODO: buka "latihan.txt" dengan mode "r", pakai f.read(),
# simpan ke variabel lalu print isinya.
# Petunjuk: isi = f.read() dilakukan DI DALAM blok with.


# --- SOAL 3: baca baris per baris + hitung ---
# TODO: hitung jumlah baris file dengan loop:
#   jumlah = 0
#   with open("latihan.txt", "r") as f:
#       for baris in f:
#           ... (tambah jumlah; pakai baris.strip() untuk buang \n)
#   print(f"Jumlah baris: {jumlah}")
# Uji: kalau SOAL 1 menulis 3 baris -> "Jumlah baris: 3"


# --- SOAL 4: mode "a" (append) ---
# TODO: buka file dengan mode "a", tambahkan 1 baris makanan baru,
# lalu baca ulang seluruh isi dan print.
# Buktikan: baris lama masih ada (beda dengan mode "w" di SOAL 1).


# --- SOAL 5: tangkap file yang tidak ada ---
# TODO: coba baca file "file_hilang.txt" yang memang tidak ada:
#   - tangkap FileNotFoundError
#   - print pesan ramah: "File catatan belum dibuat."
# Petunjuk: pola try/except dari latihan 05, exception-nya FileNotFoundError.


# --- SOAL 6: modul ---
# TODO:
#   1. tambahkan `import math` di paling atas file
#   2. print(math.sqrt(144))            -> 12.0
#   3. tambahkan `from datetime import date` di atas, lalu
#      print(date.today())              -> tanggal hari ini
# Uji: sqrt(144) harus 12.0 — perhatikan bahwa kamu memakai kode
# buatan orang lain tanpa menulisnya sendiri. Itu inti kegunaan modul.


# --- SOAL 7 (mini challenge): catatan harian ---
# TODO: buat program kecil:
#   1. minta user ketik satu kalimat (input)
#   2. tambahkan kalimat itu ke "catatan.txt" (mode "a") + \n
#   3. baca dan print seluruh isi "catatan.txt"
# Jalankan 2-3 kali dengan kalimat berbeda; buktikan catatan lama
# tidak hilang. Ini versi mini dari proyek akhir minggu (09)!
