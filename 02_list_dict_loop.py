# ============================================
# LATIHAN 2: List, Dict & Loop
# ============================================
# Cara pakai: isi bagian yang masih kosong, lalu jalankan:
#   python 02_list_dict_loop.py
# ============================================

# --- Konsep cepat ---
# list  = kumpulan data berurutan  -> nilai = [80, 90, 75]
#         akses pakai indeks: nilai[0] -> 80
# dict  = kumpulan pasangan key -> value
#         mahasiswa = {"nama": "Wenn", "umur": 21}
# loop  = menjalankan perintah berulang:
#   for x in [1, 2, 3]:
#       print(x)
# range(n) = deret angka 0 sampai n-1

# --- SOAL 1: list dasar ---
nilai = [80, 90, 75, 85, 95]

# TODO:
#   1. print nilai pertama (harus 80)
#   2. print nilai terakhir (harus 95) — pakai indeks negatif
#   3. tambahkan nilai 88 ke akhir list (pakai .append)
#   4. print jumlah elemen di list (pakai len) — harus 6
print(nilai[0])  # print nilai pertama
print(nilai[-1])  # print nilai terakhir
nilai.append(88)  # tambahkan nilai 88 ke akhir list
print(len(nilai))  # print jumlah elemen di list

# --- SOAL 2: for loop ---
# TODO: pakai for loop untuk print semua nilai satu per satu,
# contoh output:
#   Nilai 1: 80
#   Nilai 2: 90
#   dst...
# Petunjuk: pakai enumerate(nilai, start=1) biar dapat nomor urut
for i, n in enumerate(nilai, start=1):
    print(f"Nilai {i}: {n}")

# --- SOAL 3: total & rata-rata ---
# TODO:
#   1. hitung total semua nilai dengan loop (JANGAN pakai sum() dulu,
#      coba manual: mulai dari 0, tambahkan satu per satu)
#   2. hitung rata-rata (total dibagi jumlah elemen)
#   3. print keduanya dengan f-string
total = 0
for n in nilai:
    total += n
rata_rata = total / len(nilai)
print(f"Total: {total}")
print(f"Rata-rata: {rata_rata}")

# --- SOAL 4: dict dasar ---
mahasiswa = {
    "nama": "Wenn",
    "umur": 22,
    "jurusan": "Teknik Komputer",
}

# TODO:
#   1. print nama mahasiswa (akses via key "nama")
#   2. tambahkan key baru "ipk" dengan nilai 3.75
#   3. print semua key di dict (pakai .keys())
print(mahasiswa["nama"])  # print nama mahasiswa
mahasiswa["ipk"] = 3.75  # tambahkan key baru "ipk" dengan nilai 3.75
print(mahasiswa.keys())  # print semua key di

# --- SOAL 5 (mini challenge): nilai tertinggi ---
# TODO: cari nilai tertinggi di list `nilai` dengan loop
# (JANGAN pakai max() dulu, coba manual)
# print: "Nilai tertinggi: 95"
nilai_tertinggi = nilai[0]
for n in nilai:
    if n > nilai_tertinggi:
        nilai_tertinggi = n
print(f"Nilai tertinggi: {nilai_tertinggi}")