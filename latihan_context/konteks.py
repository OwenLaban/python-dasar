"""Fungsi dasar untuk mengelola konteks LLM.

Semua fungsi di sini bekerja pada level token, bukan sekadar jumlah kata.
Token adalah unit yang benar-benar dihitung oleh model.
"""

import tiktoken

ENCODING = "o200k_base"


def hitung_token(teks: str, encoding: str = ENCODING) -> int:
    """Kembalikan jumlah token dari sebuah teks.

    TODO:
    1. Ambil encoder dengan ``tiktoken.get_encoding(encoding)``.
    2. Encode ``teks``.
    3. Kembalikan panjang hasil encode.
    """
    raise NotImplementedError("TODO: implementasikan hitung_token()")


def potong_token(
    teks: str,
    max_token: int,
    overlap: int = 0,
    encoding: str = ENCODING,
) -> list[str]:
    """Potong teks menjadi beberapa bagian berdasarkan token.

    Aturan:
    - ``max_token`` harus > 0.
    - ``overlap`` harus >= 0 dan < ``max_token``.
    - Teks kosong menghasilkan list kosong.
    - Setiap potongan berisi paling banyak ``max_token`` token.
    - Potongan berikutnya memakai ``max_token - overlap`` token sebelumnya
      sebagai konteks tambahan, supaya informasi di batas potongan tidak hilang.

    Petunjuk: encode seluruh teks lebih dulu, lalu potong daftar token ID.
    Setelah itu decode setiap potongan kembali menjadi string.

    TODO: implementasikan validasi dan pemotongan.
    """
    raise NotImplementedError("TODO: implementasikan potong_token()")


def anggaran_input(
    batas_konteks: int,
    token_output: int,
    token_sistem: int = 0,
) -> int:
    """Hitung token yang tersedia untuk input setelah menyisihkan output.

    Rumus: ``batas_konteks - token_output - token_sistem``.
    Jika hasilnya <= 0, raise ``ValueError`` karena tidak ada ruang untuk input.

    TODO: implementasikan.
    """
    raise NotImplementedError("TODO: implementasikan anggaran_input()")


def pilih_strategi(jumlah_token: int, batas_input: int) -> str:
    """Pilih strategi ringkasan berdasarkan ukuran input.

    - ``"stuff"`` jika seluruh teks muat dalam ``batas_input``.
    - ``"map_reduce"`` jika tidak muat.

    TODO: implementasikan. Raise ``ValueError`` jika ``batas_input`` <= 0.
    """
    raise NotImplementedError("TODO: implementasikan pilih_strategi()")


def pangkas_riwayat(
    pesan: list[dict],
    max_token: int,
    encoding: str = ENCODING,
) -> list[dict]:
    """Pertahankan pesan terbaru yang muat dalam anggaran token.

    Setiap item pesan diasumsikan memiliki field ``content``.
    Mulai dari pesan paling baru, lalu ambil pesan sebelumnya selama masih muat.
    Jika pesan berikutnya tidak muat seluruhnya, potong isinya sesuai sisa
    anggaran, lalu berhenti. Kembalikan pesan dalam urutan kronologis semula.

    Ini adalah bentuk sederhana **compaction**: model tidak perlu melihat
    seluruh riwayat jika anggaran token sudah habis.

    TODO: implementasikan. Raise ``ValueError`` jika ``max_token`` <= 0.
    """
    raise NotImplementedError("TODO: implementasikan pangkas_riwayat()")


def gabung_ringkasan(
    ringkasan: list[str],
    max_token: int,
    encoding: str = ENCODING,
) -> str:
    """Gabungkan beberapa ringkasan menjadi satu, dengan batas token.

    Ringkasan digabung dengan newline. Jika ringkasan berikutnya tidak muat,
    potong bagian itu sesuai sisa anggaran lalu berhenti.

    TODO: implementasikan. Raise ``ValueError`` jika ``max_token`` <= 0.
    """
    raise NotImplementedError("TODO: implementasikan gabung_ringkasan()")


def main() -> None:
    teks = (
        "Context engineering adalah cara menyusun informasi yang masuk ke "
        "model. Kita perlu menghitung token, memilih sumber yang relevan, "
        "dan memadatkan riwayat agar model tidak kehilangan detail penting."
    )

    jumlah = hitung_token(teks)
    print(f"Token: {jumlah}")
    print(f"Potongan 8 token, overlap 2: {potong_token(teks, 8, 2)}")
    print(f"Anggaran input: {anggaran_input(2048, 256, 100)} token")
    print(f"Strategi: {pilih_strategi(jumlah, 20)}")


if __name__ == "__main__":
    main()
