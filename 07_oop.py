# ============================================
# LATIHAN 7: OOP Dasar (class & method)
# ============================================
# Cara pakai: isi bagian yang masih kosong, lalu jalankan:
#   python 07_oop.py
# Target: bisa membuat class sendiri + objeknya.
# ============================================

# --- Konsep cepat ---
# class = "cetakan" untuk membuat objek.
# Objek punya:
#   attribute = data yang disimpan (mis. nama, umur)
#   method    = perilaku/fungsi milik objek
#
#   class Kucing:
#       def __init__(self, nama):    # jalan otomatis saat objek dibuat
#           self.nama = nama         # self = objek itu sendiri
#
#       def suara(self):             # method; parameter pertama selalu self
#           return "Meong"
#
# Cara pakai:
#   kucingku = Kucing("Oyen")   # instansiasi = membuat objek dari class
#   print(kucingku.nama)        # akses attribute  -> Oyen
#   print(kucingku.suara())     # panggil method   -> Meong

# --- CONTOH: baca & jalankan ---
class Kucing:
    def __init__(self, nama):
        self.nama = nama

    def suara(self):
        return "Meong"


oyen = Kucing("Oyen")
print(f"{oyen.nama} bersuara: {oyen.suara()}")


# --- SOAL 1: class pertama ---
# TODO: buat class Mahasiswa dengan __init__(self, nama, umur),
# simpan keduanya sebagai attribute, dan method perkenalan(self) yang
# mengembalikan: "Aku <nama>, umur <umur> tahun."
# Lalu buat objeknya dengan namamu dan panggil perkenalan().
# Uji: print(mhs.perkenalan())  -> Aku Wenn, umur 22 tahun.
class Mahasiswa:
    def __init__(self, nama, umur):
        self.nama = nama
        self.umur = umur

    def ultah(self):
        self.umur += 1

    def perkenalan(self):
        return f"Aku {self.nama}, umur {self.umur} tahun."
print(Mahasiswa("Wenn", 22).perkenalan())
# --- SOAL 2: class dengan perilaku ---
# TODO: buat class RekeningBank dengan __init__(self, pemilik, saldo) dan:
#   - setor(self, jumlah)  -> saldo bertambah
#   - tarik(self, jumlah)  -> kalau jumlah > saldo: return False
#                             (dan saldo TIDAK berubah)
#                             kalau cukup: saldo berkurang, return True
# Uji:
#   rek = RekeningBank("Wenn", 50000)
#   print(rek.tarik(30000))   -> True
#   print(rek.tarik(30000))   -> False   (saldo sekarang cuma 20000)
#   print(rek.saldo)          -> 20000
class RekeningBank:
    def __init__(self, pemilik, saldo):
        self.pemilik = pemilik
        self.saldo = saldo

    def setor(self, jumlah):
        self.saldo += jumlah

    def tarik(self, jumlah):
        if jumlah > self.saldo:
            return False
        else:
            self.saldo -= jumlah
            return True
rek = RekeningBank("Wenn", 50000)
print(rek.tarik(30000))   # True
print(rek.tarik(30000))   # False
print(rek.saldo)          # 20000

# --- SOAL 3: method yang mengubah attribute ---
# TODO: tambah method ultah(self) ke class Mahasiswa dari SOAL 1:
# umur bertambah 1. Uji:
#   print(mhs.umur)
#   mhs.ultah()
#   print(mhs.umur)   -> lihat bedanya
# (Ya, kamu boleh mengedit class yang sudah kamu buat — itu normal!)
mhs = Mahasiswa("Wenn", 22)
print(mhs.umur)  # 22
mhs.ultah()
print(mhs.umur)  # 23

# --- SOAL 4: inheritance (pewarisan) ---
# Konsep: class anak mewarisi semua method induk, dan bisa meng-override.
# TODO: lengkapi:
#   class Hewan:
#       def __init__(self, nama): ...
#       def suara(self):
#           return "..."
#
#   class Kucing(Hewan):    # (Hewan) artinya mewarisi Hewan
#       def suara(self):
#           return "Meong"
#
#   class Anjing(Hewan):
#       def suara(self):
#           return "Guk"
#
# Lalu buat list berisi satu Kucing dan satu Anjing, dan loop print:
#   for hewan in daftar:
#       print(f"{hewan.nama}: {hewan.suara()}")
# Output: Oyen: Meong / Bruno: Guk
# Catatan: Kucing dan Anjing TIDAK menulis __init__ sendiri —
# mereka memakai __init__ milik Hewan. Itu inti dari pewarisan.
class Hewan:
    def __init__(self, nama):
        self.nama = nama

    def suara(self):
        return "..."

class Kucing(Hewan):
    def suara(self):
        return "Meong"

class Anjing(Hewan):
    def suara(self):
        return "Guk"

daftar = [Kucing("Oyen"), Anjing("Bruno")]
for hewan in daftar:
    print(f"{hewan.nama}: {hewan.suara()}")


# --- SOAL 5 (mini challenge): bekal untuk proyek 09 ---
# TODO: buat class Tugas dengan __init__(self, teks), attribute
# `selesai` mulai dari False, dan:
#   - method selesaikan(self) -> ubah selesai jadi True
#   - method __str__(self)    -> mengembalikan "[ ] teks" kalau belum
#     selesai, "[x] teks" kalau sudah selesai
# Uji:
#   tugas1 = Tugas("Belajar OOP")
#   tugas1.selesaikan()
#   print(tugas1)             -> [x] Belajar OOP
# Petunjuk: __str__ dipanggil otomatis saat objek di-print().
class Tugas:
    def __init__(self, teks):
        self.teks = teks
        self.selesai = False

    def selesaikan(self):
        self.selesai = True

    def __str__(self):
        status = "[x]" if self.selesai else "[ ]"
        return f"{status} {self.teks}"
tugas1 = Tugas("Belajar OOP")
tugas1.selesaikan()
print(tugas1)  # [x] Belajar OOP