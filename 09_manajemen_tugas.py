# ============================================
# PROYEK MINGGU 2: Manajemen Tugas (CLI)
# ============================================
# Cara pakai:
#   python 09_manajemen_tugas.py
#
# FITUR:
#   1. Lihat semua tugas
#   2. Tambah tugas baru
#   3. Tandai tugas selesai
#   4. Hapus tugas
#   5. Keluar
#
# DATA: tersimpan di tugas.json (satu folder dengan file ini) supaya
# tidak hilang saat program ditutup. Formatnya list of dict:
#   [
#     {"teks": "Belajar OOP", "selesai": true},
#     {"teks": "Latihan file I/O", "selesai": false}
#   ]
#
# MODUL: json (json.dump / json.load) dan pathlib (Path).
# JSON hanya kenal dict, list, str, int, float, bool, None.
# Karena itu objek Tugas diubah ke dict dulu lewat to_dict().
# ============================================

import json
from pathlib import Path

FILE_TUGAS = Path(__file__).parent / "tugas.json"


# --- 1. CLASS TUGAS ---
class Tugas:
    def __init__(self, teks: str):
        self.teks = teks
        self.selesai = False

    def selesaikan(self) -> None:
        self.selesai = True

    def __str__(self) -> str:
        status = "x" if self.selesai else " "
        return f"[{status}] {self.teks}"

    def to_dict(self) -> dict:
        return {"teks": self.teks, "selesai": self.selesai}


# --- 2. SIMPAN & MUAT (persistence) ---
def simpan_tugas(daftar: list[Tugas]) -> None:
    data = [t.to_dict() for t in daftar]
    with open(FILE_TUGAS, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def muat_tugas() -> list[Tugas]:
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


# --- 3. TAMPILAN & AKSI ---
def tampilkan_tugas(daftar: list[Tugas]) -> None:
    if not daftar:
        print("Belum ada tugas.")
    else:
        for i, tugas in enumerate(daftar, start=1):
            print(f"{i}. {tugas}")


def tambah_tugas(daftar: list[Tugas]) -> None:
    input_teks = input("Masukkan teks tugas: ").strip()
    if not input_teks:
        print("Teks tugas tidak boleh kosong.")
    else:
        daftar.append(Tugas(input_teks))
        print(f"Tugas '{input_teks}' berhasil ditambahkan.")
        simpan_tugas(daftar)


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


# "if __name__ == '__main__'" = jalankan main() HANYA kalau file ini
# dijalankan langsung, bukan saat di-import dari file lain.
if __name__ == "__main__":
    main()
