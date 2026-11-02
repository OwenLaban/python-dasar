"""Fungsi dasar untuk bekerja dengan embedding.

Embedding adalah representasi teks sebagai vektor angka. Makna yang mirip
berada berdekatan di ruang vektor. Di sini kita menghitung kedekatan itu
sendiri, tanpa library machine learning.
"""

import math


def dot_product(a: list[float], b: list[float]) -> float:
    """Kembalikan hasil dot product dua vektor.

    TODO:
    1. Pastikan panjang ``a`` dan ``b`` sama; jika tidak, raise ``ValueError``.
    2. Kalikan elemen pada posisi yang sama, lalu jumlahkan.
    """
    if len(a) != len(b):
        raise ValueError("Panjang vektor harus sama")
    return sum(x * y for x, y in zip(a, b))


def norm(v: list[float]) -> float:
    """Kembalikan panjang (L2 norm) sebuah vektor.

    Rumus: ``sqrt(x1**2 + x2**2 + ... + xn**2)``.
    Vektor kosong memiliki norm 0.0.
    """
    return math.hypot(*v)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Kembalikan cosine similarity antara dua vektor, dari -1 sampai 1.

    Nilai 1 berarti arah sama, 0 berarti tegak lurus, -1 berarti berlawanan.

    TODO:
    1. Validasi panjang vektor.
    2. Hitung ``dot_product(a, b) / (norm(a) * norm(b))``.
    3. Raise ``ValueError`` jika salah satu vektor nol (tidak punya arah).
    """
    if len(a) != len(b):
        raise ValueError("Panjang vektor harus sama")
    norm_a = norm(a)
    norm_b = norm(b)
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vektor nol tidak memiliki arah")
    return dot_product(a, b) / (norm_a * norm_b)


def normalisasi(v: list[float]) -> list[float]:
    """Kembalikan vektor dengan panjang 1.

    TODO: bagi setiap elemen dengan ``norm(v)``. Raise ``ValueError`` jika
    vektor nol, karena pembagian dengan nol tidak terdefinisi.
    """
    n = norm(v)
    if n == 0:
        raise ValueError("Vektor nol tidak dapat dinormalisasi")
    return [x / n for x in v]


def cari_terdekat(
    query_vec: list[float],
    kandidat: list[dict],
    k: int = 3,
) -> list[dict]:
    """Urutkan kandidat berdasarkan cosine similarity terhadap query.

    Setiap kandidat adalah dict dengan minimal field ``teks``, ``topik``, dan
    ``vektor``. Kembalikan maksimal ``k`` dict berisi ``teks``, ``topik``, dan
    ``skor``, diurutkan dari skor tertinggi.

    TODO:
    1. Validasi ``k > 0``.
    2. Hitung cosine similarity untuk setiap kandidat.
    3. Urutkan menurun, ambil ``k`` teratas.
    4. Jangan mengubah list kandidat asli.
    """
    if k <= 0:
        raise ValueError("k harus > 0")
    hasil = []
    for item in kandidat:
        skor = cosine_similarity(query_vec, item["vektor"])
        hasil.append({"teks": item["teks"], "topik": item["topik"], "skor": skor})
    hasil.sort(key=lambda x: x["skor"], reverse=True)
    return hasil[:k]


def precision_at_k(hasil: list[dict], topik: str, k: int | None = None) -> float:
    """Hitung proporsi hasil teratas yang topiknya sesuai.

    Contoh: 2 dari 3 hasil teratas bertopik ``"teknologi"`` → 0.666...
    Jika ``k`` tidak diberikan, pakai seluruh hasil. Jika tidak ada hasil,
    kembalikan 0.0. Jika ``k`` diberikan, nilainya harus lebih besar dari 0.
    """
    if k is not None and k <= 0:
        raise ValueError("k harus > 0")
    if not hasil:
        return 0.0
    if k is None:
        k = len(hasil)
    else:
        k = min(k, len(hasil))
    relevan = sum(1 for item in hasil[:k] if item["topik"] == topik)
    return relevan / k
