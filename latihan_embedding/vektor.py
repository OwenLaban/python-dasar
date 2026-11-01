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
    raise NotImplementedError("TODO: implementasikan dot_product()")


def norm(v: list[float]) -> float:
    """Kembalikan panjang (L2 norm) sebuah vektor.

    Rumus: ``sqrt(x1**2 + x2**2 + ... + xn**2)``.
    Vektor kosong memiliki norm 0.0.
    """
    raise NotImplementedError("TODO: implementasikan norm()")


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Kembalikan cosine similarity antara dua vektor, dari -1 sampai 1.

    Nilai 1 berarti arah sama, 0 berarti tegak lurus, -1 berarti berlawanan.

    TODO:
    1. Validasi panjang vektor.
    2. Hitung ``dot_product(a, b) / (norm(a) * norm(b))``.
    3. Raise ``ValueError`` jika salah satu vektor nol (tidak punya arah).
    """
    raise NotImplementedError("TODO: implementasikan cosine_similarity()")


def normalisasi(v: list[float]) -> list[float]:
    """Kembalikan vektor dengan panjang 1.

    TODO: bagi setiap elemen dengan ``norm(v)``. Raise ``ValueError`` jika
    vektor nol, karena pembagian dengan nol tidak terdefinisi.
    """
    raise NotImplementedError("TODO: implementasikan normalisasi()")


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
    raise NotImplementedError("TODO: implementasikan cari_terdekat()")


def precision_at_k(hasil: list[dict], topik: str, k: int | None = None) -> float:
    """Hitung proporsi hasil teratas yang topiknya sesuai.

    Contoh: 2 dari 3 hasil teratas bertopik ``"teknologi"`` → 0.666...
    Jika ``k`` tidak diberikan, pakai seluruh hasil. Jika tidak ada hasil,
    kembalikan 0.0.
    """
    raise NotImplementedError("TODO: implementasikan precision_at_k()")
