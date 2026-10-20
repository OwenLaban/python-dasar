# ============================================
# PROYEK MINGGU 2: Manajemen Tugas (CLI)
# ============================================
# Cara pakai: isi semua TODO, lalu jalankan:
#   python 09_manajemen_tugas.py
#
# FITUR:
#   1. Lihat semua tugas
#   2. Tambah tugas baru
#   3. Tandai tugas selesai
#   4. Hapus tugas
#   5. Keluar
#
# DATA: tersimpan di tugas.json supaya tidak hilang saat program ditutup.
# Formatnya list of dict:
#   [
#     {"teks": "Belajar OOP", "selesai": true},
#     {"teks": "Latihan file I/O", "selesai": false}
#   ]
#
# MODUL BARU: json
#   json.dump(data, f)  -> tulis objek Python (list/dict/str/int/bool) ke file
#   json.load(f)        -> baca file JSON jadi objek Python
#   JSON hanya kenal dict, list, str, int, float, bool, None.
#   Karena itu objek Tugas harus diubah ke dict dulu lewat to_dict().
#
# KRITERIA LULUS (uji sendiri setelah semua TODO terisi):
#   [ ] Tambah 2 tugas -> keluar -> jalankan lagi -> tugas masih ada
#   [ ] Tandai selesai -> terlihat [x], dan tetap [x] setelah restart
#   [ ] Pilih menu bukan angka (mis. "abc") -> muncul pesan, tidak crash
#   [ ] Pilih nomor tugas yang tidak ada (mis. 99) -> pesan ramah, tidak crash
#   [ ] Hapus tugas -> hilang, dan tetap hilang setelah restart
#   [ ] Semua fungsi punya type hint
# ============================================

import json

FILE_TUGAS = "tugas.json"
from pathlib import Path
FILE_TUGAS = Path(__file__).parent / "tugas.json"
if not Path(FILE_TUGAS).exists():
    with open(FILE_TUGAS, "w") as f:
        json.dump([], f)  # buat file kosong kalau belum ada    

# --- 1. CLASS TUGAS ---
# TODO: lengkapi class ini (mirip latihan 07 SOAL 5).
# Bedanya: tambahkan to_dict(self) untuk kebutuhan JSON.
class Tugas:
    def __init__(self, teks: str):
        self.teks = teks
        self.selesai = False

    def selesaikan(self) -> None:
        self.selesai = True
        # TODO: ubah self.selesai jadi True
        pass

    def __str__(self) -> str:
        # TODO: kembalikan "[ ] teks" kalau belum selesai,
        # "[x] teks" kalau sudah selesai
        status = "x" if self.selesai else " "
        return f"[{status}] {self.teks}"

    def to_dict(self) -> dict:
        # TODO: kembalikan {"teks": ..., "selesai": ...}
        return {"teks": self.teks, "selesai": self.selesai}


# --- 2. SIMPAN & MUAT (persistence) ---
def simpan_tugas(daftar: list[Tugas]) -> None:
    data = [t.to_dict() for t in daftar]
    with open(FILE_TUGAS, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # TODO:
    #   1. ubah tiap Tugas jadi dict: data = [t.to_dict() for t in daftar]
    #   2. tulis ke FILE_TUGAS:
    #      with open(FILE_TUGAS, "w") as f:
    #          json.dump(data, f, indent=2, ensure_ascii=False)
    pass


def muat_tugas() -> list[Tugas]:
    json_data = []
    try:
        with open(FILE_TUGAS, "r") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        return []
    hasil = []
    for item in json_data:
        t = Tugas(item["teks"])
        t.selesai = item["selesai"]
        hasil.append(t)
    return hasil         

    # TODO:
    #   1. buka FILE_TUGAS mode "r", baca dengan json.load(f)
    #   2. tangkap FileNotFoundError -> return []
    #      (file belum ada artinya belum ada tugas, bukan error)
    #   3. ubah tiap dict jadi objek Tugas, termasuk set .selesai-nya
    #      Petunjuk: t = Tugas(item["teks"]); t.selesai = item["selesai"]

# --- 3. TAMPILAN & AKSI ---
def tampilkan_tugas(daftar: list[Tugas]) -> None:
    if not daftar:
        print("Belum ada tugas.")
    else:
        for i, tugas in enumerate(daftar, start=1):
            print(f"{i}. {tugas}")

    # TODO:
    #   - kalau daftar kosong: print "Belum ada tugas."
    #   - kalau ada: loop enumerate(daftar, start=1) dan
    #     print f"{i}. {tugas}"



def tambah_tugas(daftar: list[Tugas]) -> None:
    input_teks = input("Masukkan teks tugas: ").strip()
    if not input_teks:
        print("Teks tugas tidak boleh kosong.")
    else:
        daftar.append(Tugas(input_teks))
        print(f"Tugas '{input_teks}' berhasil ditambahkan.")
        simpan_tugas(daftar)
    # TODO:
    #   1. minta input teks tugas
    #   2. kalau kosong setelah .strip(): print "Teks tugas tidak boleh kosong."
    #   3. kalau ada: daftar.append(Tugas(teks)), lalu print konfirmasi
    #   4. panggil simpan_tugas(daftar) supaya langsung tersimpan
    pass


def selesaikan_tugas(daftar: list[Tugas]) -> None:
    tampilkan_tugas(daftar)
    input_nomor = input("Masukkan nomor tugas yang selesai: ").strip()
    try:
        nomor = int(input_nomor)
        if 1 <= nomor <= len(daftar):
            daftar[nomor - 1].selesaikan()
            print(f"Tugas '{daftar[nomor - 1].teks}' ditandai selesai.")
            simpan_tugas(daftar)
        else:
            print("Nomor tugas tidak valid.")
    except ValueError:
        print("Nomor tugas harus berupa angka.")
    # TODO:
    #   1. panggil tampilkan_tugas(daftar)
    #   2. minta input nomor tugas, konversi ke int, tangkap ValueError
    #   3. cek nomor valid (1 sampai len(daftar)); kalau tidak, print pesan ramah
    #   4. daftar[nomor - 1].selesaikan()
    #   5. panggil simpan_tugas(daftar)
    pass


def hapus_tugas(daftar: list[Tugas]) -> None:
    tampilkan_tugas(daftar)
    input_nomor = input("Masukkan nomor tugas yang ingin dihapus: ").strip()
    try:
        nomor = int(input_nomor)
        if 1 <= nomor <= len(daftar):
            tugas_dihapus = daftar.pop(nomor - 1)
            print(f"Tugas '{tugas_dihapus.teks}' berhasil dihapus.")
            simpan_tugas(daftar)
        else:
            print("Nomor tugas tidak valid.")
    except ValueError:
        print("Nomor tugas harus berupa angka.")
    # TODO: seperti selesaikan_tugas, tapi aksinya:
    # daftar.pop(nomor - 1) lalu simpan_tugas(daftar)
    pass


# --- 4. MENU UTAMA ---
def main() -> None:
    daftar = muat_tugas()
    while True:
        print("\n===== MANAJEMEN TUGAS =====")
        print("1. Lihat tugas")
        print("2. Tambah tugas")
        print("3. Tandai selesai")
        print("4. Hapus tugas")
        print("5. Keluar")

        input_pilihan = input("Pilih menu (1-5): ").strip()
        try:
            pilihan = int(input_pilihan)
        except ValueError:
            print("Pilihan harus berupa angka.")
            continue
        
        
        if pilihan == 1:
            tampilkan_tugas(daftar)
        elif pilihan == 2:
            tambah_tugas(daftar)
        elif pilihan == 3:
            selesaikan_tugas(daftar)
        elif pilihan == 4:
            hapus_tugas(daftar)
        elif pilihan == 5:
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid.")
        
        # TODO:
        #   1. minta input pilihan (string), konversi ke int,
        #      tangkap ValueError -> print "Pilihan harus berupa angka." lalu continue
        #   2. panggil fungsi sesuai pilihan:
        #      1 -> tampilkan_tugas(daftar)
        #      2 -> tambah_tugas(daftar)
        #      3 -> selesaikan_tugas(daftar)
        #      4 -> hapus_tugas(daftar)
        #      5 -> break
        #      selain 1-5 -> print "Pilihan tidak valid."
        #
        # Sementara: break di bawah ini cuma supaya skeleton tidak
        # infinite loop. HAPUS setelah TODO di atas selesai dikerjakan.



# "if __name__ == '__main__'" = jalankan main() HANYA kalau file ini
# dijalankan langsung, bukan saat di-import dari file lain.
# Pola ini standar di semua program Python — hafalkan.
if __name__ == "__main__":
    main()
