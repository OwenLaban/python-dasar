# ============================================
# LATIHAN 5: Error Handling (try/except)
# ============================================
# Cara pakai: isi bagian yang masih kosong, lalu jalankan:
#   python 05_error_handling.py
# Target: program tetap jalan walau ada operasi yang gagal.
# ============================================

# --- Konsep cepat ---
# Error (exception) = masalah yang muncul SAAT program berjalan.
# Tanpa penanganan, program langsung berhenti + muncul traceback.
#
# try/except = "coba jalankan; kalau error, tangani begini":
#   try:
#       x = int("abc")        # baris yang mungkin error
#   except ValueError:
#       x = None              # jalan kalau ValueError terjadi
#
# Exception yang umum:
#   ValueError        -> konversi gagal, mis. int("abc")
#   ZeroDivisionError -> pembagian nol
#   KeyError          -> key tidak ada di dict
#   FileNotFoundError -> file tidak ditemukan (dipakai di latihan 06)
#
# raise = melempar error sendiri kalau data tidak valid.
# except ValueError as e = tangkap errornya, pesannya bisa diambil dari e.
# finally = blok yang SELALU jalan di akhir (dibahas di bawah).

# --- SOAL 1: tangkap ValueError ---
# TODO: buat fungsi aman_int(teks) yang:
#   - mengembalikan int(teks) kalau berhasil
#   - mengembalikan None kalau konversi gagal
# Uji setelah selesai:
#   print(aman_int("25"))    -> 25
#   print(aman_int("abc"))   -> None
# Petunjuk: letakkan int(teks) di dalam try, dan return None di except.
def aman_int(teks):
    try:
        return int(teks)
    except ValueError:
        return None
print(aman_int("25"))    # -> 25
print(aman_int("abc"))   # -> None
 
# --- SOAL 2: pembagian aman ---
# TODO: buat fungsi bagi_aman(a, b) yang:
#   - mengembalikan a / b kalau berhasil
#   - mengembalikan None kalau b = 0 (tangkap ZeroDivisionError)
# Uji:
#   print(bagi_aman(10, 2))  -> 5.0
#   print(bagi_aman(10, 0))  -> None
def bagi_aman(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None 
print(bagi_aman(10, 2))  # -> 5.0
print(bagi_aman(10, 0))  # -> None
# --- SOAL 3: input user yang tahan banting ---
# TODO: minta user mengetik angka dengan input(), lalu:
#   - kalau BUKAN angka -> print "Itu bukan angka!"
#   - kalau angka       -> print hasilnya dikali 2
# Susun pakai try/except (bukan if .isdigit() ya).
# Contoh: user ketik "21"  -> Hasil x2: 42
#         user ketik "abc" -> Itu bukan angka!
input_user = input("Masukkan angka: ")
try:
    angka = int(input_user)
    print(f"Hasil x2: {angka * 2}")
except ValueError:
    print("Itu bukan angka!")   

# --- SOAL 4: tangkap dua jenis error ---
# TODO: buat fungsi rata_rata_key(data, key) yang mengembalikan
# data[key] dibagi len(data):
#   - kalau key tidak ada (KeyError) -> return None
#   - kalau data kosong (ZeroDivisionError) -> return None
# Uji:
#   print(rata_rata_key({"nilai": 90}, "nilai"))  -> 90.0
#   print(rata_rata_key({"nilai": 90}, "ipk"))    -> None
#   print(rata_rata_key({}, "nilai"))             -> None
# Petunjuk: boleh dua blok `except` terpisah, atau satu baris
# except (KeyError, ZeroDivisionError).
def rata_rata_key(data, key):
    try:
        return data[key] / len(data)
    except (KeyError, ZeroDivisionError):
        return None
print(rata_rata_key({"nilai": 90}, "nilai"))  # -> 90.0
print(rata_rata_key({"nilai": 90}, "ipk"))    # -> None
print(rata_rata_key({}, "nilai"))             # -> None

# --- SOAL 5 (mini challenge): validasi dengan raise ---
# TODO: buat fungsi validasi_umur(umur) yang:
#   - raise ValueError("Umur tidak boleh negatif") kalau umur < 0
#   - mengembalikan umur kalau valid
# Lalu panggil keduanya:
#   print(validasi_umur(21))  -> 21
#   panggil validasi_umur(-5) di dalam try/except ValueError as e,
#   lalu print(f"Error: {e}") -> Error: Umur tidak boleh negatif
def validasi_umur(umur):
    if umur < 0:
        raise ValueError("Umur tidak boleh negatif")
    return umur
print(validasi_umur(21))  # -> 21
try:
    validasi_umur(-5)
except ValueError as e:
    print(f"Error: {e}")  # -> Error: Umur tidak boleh negatif
    

# --- BONUS (baca saja): finally ---
# try:
#     ...kode yang mungkin error...
# except ...:
#     ...penanganan...
# finally:
#     print("blok ini selalu jalan, error ataupun tidak")
#
# Kegunaan: "bersih-bersih" seperti menutup file/koneksi.
# Konsep ini nyambung ke latihan 06 (keyword `with`).
