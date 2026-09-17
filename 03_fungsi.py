# ============================================
# LATIHAN 3: Fungsi
# ============================================
# Cara pakai: isi bagian yang masih kosong, lalu jalankan:
#   python 03_fungsi.py
# ============================================

# --- Konsep cepat ---
# Fungsi = blok kode yang bisa dipakai berulang. Struktur:
#   def nama_fungsi(parameter):
#       # kerjakan sesuatu
#       return hasil     # return = nilai yang dikembalikan
# Fungsi tanpa return otomatis mengembalikan None.

# --- CONTOH: fungsi sudah jadi, baca & jalankan ---
def luas_persegi(sisi):
    """Hitung luas persegi = sisi * sisi."""
    return sisi * sisi

print(f"Luas persegi sisi 5: {luas_persegi(5)}")  # harus 25


# --- SOAL 1: fungsi sapa ---
# TODO: buat fungsi sapa(nama) yang mengembalikan teks
#   "Halo, <nama>! Selamat belajar."
# lalu panggil dan print hasilnya dengan nama kamu
def sapa(nama):
    return f"Halo, {nama}! Selamat belajar."

print(sapa("Wenn"))

# --- SOAL 2: fungsi dengan 2 parameter ---
# TODO: buat fungsi luas_segitiga(alas, tinggi) yang mengembalikan
#   alas * tinggi / 2
# lalu panggil dengan alas=10, tinggi=4 -> harus 20.0
def luas_segitiga(alas, tinggi):
    return alas * tinggi / 2

print(luas_segitiga(10, 4))
# --- SOAL 3: default parameter ---
# TODO: buat fungsi pangkat(angka, pangkat=2) -> angka dipangkatkan
#   pangkat=2 itu default: kalau pemanggilan tanpa argumen kedua,
#   otomatis dipangkatkan 2.
# Uji dua-duanya:
#   pangkat(3)       -> 9
#   pangkat(3, 3)    -> 27
def pangkat(angka, pangkat=2):
    return angka ** pangkat

print(pangkat(3))
print(pangkat(3, 3))
# --- SOAL 4: fungsi + kondisi if ---
# Konsep baru: if/else untuk pengambilan keputusan
#   if umur >= 18:
#       print("dewasa")
#   else:
#       print("anak-anak")
def usia(umur):
    if umur >= 18:
        print("dewasa")
    else:
        print("anak-anak")

usia(22)
# TODO: buat fungsi cek_genap(angka) yang mengembalikan
#   True kalau angka genap, False kalau ganjil
# Petunjuk: operator % = sisa bagi. 4 % 2 -> 0 (genap)
# Uji: cek_genap(4) -> True, cek_genap(7) -> False
def cek_genap(angka):
    if angka % 2 == 0:
        return True
    return False

print(cek_genap(14))
# --- SOAL 5 (mini challenge): konversi suhu ---
# TODO: buat fungsi celsius_ke_fahrenheit(celsius) yang mengembalikan
#   celsius * 9/5 + 32
# Uji:
#   celsius_ke_fahrenheit(0)   -> 32.0
#   celsius_ke_fahrenheit(100) -> 212.0
# Ini jadi fondasi proyek utama sesi ini!
def celcius_ke_fahrenheit(celcius):
    return celcius * 9/5 + 32

print(celcius_ke_fahrenheit(0))
print(celcius_ke_fahrenheit(100.0))