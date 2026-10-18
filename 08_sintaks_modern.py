# ============================================
# LATIHAN 8: Sintaks Modern
# (f-string lanjutan, list comprehension, type hints)
# ============================================
# Cara pakai: isi bagian yang masih kosong, lalu jalankan:
#   python 08_sintaks_modern.py
# ============================================

# --- Konsep cepat: f-string lanjutan ---
# Sejauh ini kamu pakai f"{nilai}". Ada lagi "format spec" setelah titik dua:
#   f"{3.14159:.2f}"   -> 3.14        (2 angka di belakang koma)
#   f"{1250000:,}"     -> 1,250,000   (pemisah ribuan)
#   f"{0.856:.1%}"     -> 85.6%       (persen)
#   f"{umur=}"         -> umur=22     (mode debug: cetak nama + nilai)
#
# --- Konsep cepat: list comprehension ---
# Cara singkat membuat list baru dari list/range lain:
#   [x * x for x in range(1, 6)]           -> [1, 4, 9, 16, 25]
#   [x for x in range(10) if x % 2 == 0]   -> [0, 2, 4, 6, 8]
#   ["Lulus" if n >= 80 else "Gagal" for n in nilai]
# Dibaca: "untuk setiap x, buat x * x". Bisa tambah `if` untuk filter.
#
# --- Konsep cepat: type hints ---
# Menuliskan tipe data yang diharapkan — dokumentasi hidup, tidak wajib:
#   def bagi(a: float, b: float) -> float:
#   umur: int = 22
# Editor (VS Code) membacanya untuk autocomplete + peringatan dini.


# --- SOAL 1: format uang ---
# TODO: harga = 1250000.5. Print dengan format "Rp1,250,000.50"
# (pakai f-string + format spec). Lalu print sekali lagi dengan
# f"{harga=}" (mode debug) — perhatikan bedanya.
# Petunjuk: f"Rp{harga:,.2f}"


# --- SOAL 2: comprehension dasar ---
# TODO: buat list berisi kuadrat dari 1 sampai 10 dengan SATU baris
# comprehension, lalu print.
# Uji: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# Butuh merasa bedanya? Tulis dulu versi loop for-nya (3 baris), baru
# ganti jadi comprehension dan bandingkan panjangnya.


# --- SOAL 3: comprehension + filter ---
# TODO: dari angka 1-20, buat list berisi angka GENAP saja
# (comprehension + if). Uji: [2, 4, 6, ..., 20]


# --- SOAL 4: transformasi list ---
# kata = ["python", "ai", "rag", "agent"]
# TODO:
#   1. buat list baru berisi tiap kata di-uppercase (comprehension)
#      Uji: ['PYTHON', 'AI', 'RAG', 'AGENT']
#   2. bonus: buat list berisi kata yang panjangnya LEBIH DARI 3 saja
#      sekaligus di-uppercase (filter + transform dalam satu baris)


# --- SOAL 5: type hints ---
# TODO:
#   1. tulis ulang fungsi cek_genap dari latihan 03 dengan hint:
#      def cek_genap(angka: int) -> bool:
#   2. tulis ulang fungsi aman_int dari latihan 05 dengan hint:
#      def aman_int(teks: str) -> int | None:
#      (# "int | None" = hasilnya boleh int ATAU None)
# Uji: print(cek_genap(4)) -> True


# --- SOAL 6 (mini challenge): gabungkan semua ---
# TODO: buat fungsi ringkas(nilai: list[float]) -> str yang:
#   - menghitung total dan rata-rata (boleh pakai sum() sekarang)
#   - mengembalikan: "Total: 513 (rata-rata: 85.50)"
#     (pakai f-string + .2f untuk rata-ratanya)
# Uji: print(ringkas([80, 90, 75, 85, 95, 88]))
