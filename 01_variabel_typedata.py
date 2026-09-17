# ============================================
# LATIHAN 1: Variabel & Tipe Data + f-string
# ============================================
# Cara pakai: isi bagian yang masih kosong, lalu jalankan:
#   python 01_variabel_typedata.py
# Target: semua print menghasilkan output yang benar.
# ============================================

# --- Konsep cepat ---
# Variabel = wadah nyimpan data. Tipe dasar Python:
#   int   -> bilangan bulat        (mis. 21)
#   float -> bilangan desimal      (mis. 170.5)
#   str   -> teks                  (mis. "Wenn")
#   bool  -> True / False
# f-string = cara nulis teks yang isinya variabel:
#   f"Halo, {nama}!"

# --- SOAL 1: buat 4 variabel ---
# TODO: buat variabel:
#   nama      (str)   -> nama kamu
#   umur      (int)   -> umur kamu
#   tinggi    (float) -> tinggi badan (cm)
#   mahasiswa (bool)  -> True kalau kamu mahasiswa


# --- SOAL 2: tampilkan dengan f-string ---
# TODO: print satu kalimat berisi semua variabel, contoh format:
#   "Halo, aku Wenn, umur 21 tahun, tinggi 170.5 cm, status mahasiswa: True"


# --- SOAL 3: cek tipe variabel ---
# TODO: print tipe dari umur dan tinggi dengan type(), contoh:
#   <class 'int'>
#   <class 'float'>


# --- SOAL 4: konversi tipe ---
angka_teks = "25"

# TODO: konversi angka_teks jadi int, simpan di angka_asli
# lalu print hasilnya dikali 4 (harus 100, bukan "2525")


# --- SOAL 5 (mini challenge): input dari user ---
# TODO:
#   1. tanya nama user dengan input()
#   2. tanya tahun lahir user dengan input()
#   3. hitung perkiraan umur tahun ini (pakai 2026)
#   4. print: "Halo <nama>, kamu sekitar <umur> tahun"
# Petunjuk: input() selalu menghasilkan str, jadi perlu konversi!
