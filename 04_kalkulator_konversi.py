# ============================================
# PROYEK UTAMA SESI 1: Kalkulator + Konverter Suhu
# ============================================
# Gabungan materi sesi 1: fungsi + return, if/else,
# while loop, input(), f-string, konversi tipe
#
# Jalankan:
#   python 04_kalkulator_konversi.py
# ============================================


# --- Fungsi aritmetika: semua MENGEMBALIKAN hasil (return) ---
def tambah(a, b):
    return a + b

def kurang(a, b):
    return a - b

def kali(a, b):
    return a * b

def bagi(a, b):
    # None = tanda hasil tidak ada (bukan string "None"!)
    if b == 0:
        return None
    return a / b


# --- Konverter suhu ---
def celcius_ke_fahrenheit(celcius):
    return celcius * 9/5 + 32

def celcius_ke_kelvin(celcius):
    return celcius + 273.15


# --- Menu utama ---
# while True = loop tanpa henti, break = keluar dari loop.
# Menu di dalam loop biar muncul lagi tiap putaran.
while True:
    print("=====KALKULATOR=====")
    print("1. Tambah")
    print("2. Kurang")
    print("3. Kali")
    print("4. Bagi")
    print("5. C -> F")
    print("6. C -> K")
    print("7. Keluar")

    pilihan = int(input("Pilih = "))

    if pilihan == 7:
        break
    elif pilihan == 1:
        a = float(input("Input Nilai a : "))
        b = float(input("Input Nilai b : "))
        hasil = tambah(a, b)
        print(f"Hasil = {hasil}")
    elif pilihan == 2:
        a = float(input("Input Nilai a : "))
        b = float(input("Input Nilai b : "))
        hasil = kurang(a, b)
        print(f"Hasil = {hasil}")
    elif pilihan == 3:
        a = float(input("Input Nilai a : "))
        b = float(input("Input Nilai b : "))
        hasil = kali(a, b)
        print(f"Hasil = {hasil}")
    elif pilihan == 4:
        a = float(input("Input Nilai a : "))
        b = float(input("Input Nilai b : "))
        hasil = bagi(a, b)
        # cek nilai kosong: hasil is None (bukan == "None")
        if hasil is None:
            print("Tidak bisa dibagi nol!")
        else:
            print(f"Hasil = {hasil}")
    elif pilihan == 5:
        a = float(input("Input Nilai suhu : "))
        hasil = celcius_ke_fahrenheit(a)
        print(f"Hasil = {hasil}")
    elif pilihan == 6:
        a = float(input("Input Nilai suhu : "))
        hasil = celcius_ke_kelvin(a)
        print(f"Hasil = {hasil}")
