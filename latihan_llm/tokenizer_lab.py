# ============================================
# LATIHAN 14: Tokenizer & Context Window
# ============================================
# Jalankan dari folder python-dasar (venv aktif):
#   python -m latihan_llm.tokenizer_lab
#
# Lengkapi 4 fungsi TODO di bawah.
# ============================================

import tiktoken

ENCODING = "o200k_base"


def hitung_token(teks: str, encoding: str = ENCODING) -> int:
    """Kembalikan jumlah token dari teks.

    TODO:
    1. Buat tokenizer: enc = tiktoken.get_encoding(encoding)
    2. Encode teks: ids = enc.encode(teks)
    3. Kembalikan panjang ids
    """
    raise NotImplementedError("TODO: lengkapi hitung_token")


def pecah_token(teks: str, encoding: str = ENCODING) -> list[str]:
    """Kembalikan daftar potongan token sebagai string.

    TODO:
    1. Encode teks menjadi list id token.
    2. Decode setiap id menjadi string: enc.decode([id])
    3. Kembalikan list potongan tersebut.

    Contoh bentuk hasil: ['kem', 'erde', 'kaan']
    """
    raise NotImplementedError("TODO: lengkapi pecah_token")


def bandingkan(teks_a: str, teks_b: str, encoding: str = ENCODING) -> dict:
    """Bandingkan jumlah token dua teks.

    TODO: kembalikan dict dengan bentuk:
    {
        "token_a": ...,
        "token_b": ...,
        "selisih": ...,       # selisih absolut
        "lebih_boros": ...,   # "A", "B", atau "sama"
    }
    """
    raise NotImplementedError("TODO: lengkapi bandingkan")


def muat_dalam_context(teks: str, batas_token: int, encoding: str = ENCODING) -> bool:
    """True kalau jumlah token teks <= batas_token."""
    raise NotImplementedError("TODO: lengkapi muat_dalam_context")


def main() -> None:
    teks_a = "Halo, saya sedang belajar menjadi AI Engineer."
    teks_b = "Hello, I am learning to become an AI Engineer."

    hasil = bandingkan(teks_a, teks_b)

    print("=== Perbandingan ===")
    print(f"A: {hasil['token_a']} token -> {teks_a}")
    print(f"B: {hasil['token_b']} token -> {teks_b}")
    print(f"Selisih: {hasil['selisih']} token | lebih boros: {hasil['lebih_boros']}")

    print("\n=== Pecahan token ===")
    for kata in ["kemerdekaan", "ketidaksempurnaan", "AI Engineer"]:
        pieces = pecah_token(kata)
        print(f"{kata!r}: {len(pieces)} token -> {pieces}")

    print("\n=== Context window ===")
    print(f"Teks A muat dalam 8.000 token? {muat_dalam_context(teks_a, 8000)}")
    print(f"Teks A muat dalam 5 token? {muat_dalam_context(teks_a, 5)}")


if __name__ == "__main__":
    main()
