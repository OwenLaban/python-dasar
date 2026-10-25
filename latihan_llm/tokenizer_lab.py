# ============================================
# LATIHAN 14: Tokenizer & Context Window
# ============================================
# Jalankan dari folder python-dasar (venv aktif):
#   python -m latihan_llm.tokenizer_lab
# ============================================

import tiktoken

ENCODING = "o200k_base"


def hitung_token(teks: str, encoding: str = ENCODING) -> int:
    """Kembalikan jumlah token dari teks."""
    enc = tiktoken.get_encoding(encoding)
    ids = enc.encode(teks)
    return len(ids)


def pecah_token(teks: str, encoding: str = ENCODING) -> list[str]:
    """Kembalikan daftar potongan token sebagai string."""
    enc = tiktoken.get_encoding(encoding)
    ids = enc.encode(teks)
    return [enc.decode([id]) for id in ids]


def bandingkan(teks_a: str, teks_b: str, encoding: str = ENCODING) -> dict:
    """Bandingkan jumlah token dua teks."""
    token_a = hitung_token(teks_a, encoding)
    token_b = hitung_token(teks_b, encoding)
    selisih = abs(token_a - token_b)
    if token_a > token_b:
        lebih_boros = "A"
    elif token_b > token_a:
        lebih_boros = "B"
    else:
        lebih_boros = "sama"
    return {
        "token_a": token_a,
        "token_b": token_b,
        "selisih": selisih,
        "lebih_boros": lebih_boros,
    }


def muat_dalam_context(teks: str, batas_token: int, encoding: str = ENCODING) -> bool:
    """True kalau jumlah token teks <= batas_token."""
    return hitung_token(teks, encoding) <= batas_token


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
