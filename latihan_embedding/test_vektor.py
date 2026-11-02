"""Test fungsi vektor dan semantic search. Tidak memanggil model atau jaringan."""

import math

import pytest

from latihan_embedding import vektor

KANDIDAT = [
    {"teks": "A", "topik": "x", "vektor": [1.0, 0.0]},
    {"teks": "B", "topik": "y", "vektor": [0.8, 0.6]},
    {"teks": "C", "topik": "x", "vektor": [0.0, 1.0]},
]


def test_dot_product():
    assert vektor.dot_product([1, 2, 3], [4, 5, 6]) == 32


def test_dot_product_panjang_beda():
    with pytest.raises(ValueError):
        vektor.dot_product([1, 2], [1, 2, 3])


def test_norm():
    assert math.isclose(vektor.norm([3, 4]), 5.0)
    assert vektor.norm([]) == 0.0


def test_cosine_similarity_arah_sama():
    assert math.isclose(vektor.cosine_similarity([1, 2], [2, 4]), 1.0)


def test_cosine_similarity_tegak_lurus():
    assert math.isclose(vektor.cosine_similarity([1, 0], [0, 1]), 0.0)


def test_cosine_similarity_berlawanan():
    assert math.isclose(vektor.cosine_similarity([1, 0], [-1, 0]), -1.0)


def test_cosine_similarity_vektor_nol():
    with pytest.raises(ValueError):
        vektor.cosine_similarity([0, 0], [1, 2])


def test_cosine_similarity_panjang_beda():
    with pytest.raises(ValueError):
        vektor.cosine_similarity([1, 2], [1, 2, 3])


def test_normalisasi_panjang_satu():
    hasil = vektor.normalisasi([3, 4])

    assert math.isclose(vektor.norm(hasil), 1.0)
    assert hasil == pytest.approx([0.6, 0.8])


def test_normalisasi_vektor_nol():
    with pytest.raises(ValueError):
        vektor.normalisasi([0, 0])


def test_cari_terdekat_urutan_skor():
    hasil = vektor.cari_terdekat([1, 0], KANDIDAT, k=3)

    assert [item["teks"] for item in hasil] == ["A", "B", "C"]
    assert hasil[0]["skor"] == pytest.approx(1.0)
    assert hasil[1]["skor"] == pytest.approx(0.8)


def test_cari_terdekat_membatasi_k():
    hasil = vektor.cari_terdekat([1, 0], KANDIDAT, k=2)

    assert len(hasil) == 2
    assert [item["teks"] for item in hasil] == ["A", "B"]


def test_cari_terdekat_tidak_mengubah_kandidat():
    sebelum = [(item["teks"], tuple(item["vektor"])) for item in KANDIDAT]

    vektor.cari_terdekat([1, 0], KANDIDAT, k=2)

    sesudah = [(item["teks"], tuple(item["vektor"])) for item in KANDIDAT]
    assert sesudah == sebelum


def test_cari_terdekat_k_invalid():
    with pytest.raises(ValueError):
        vektor.cari_terdekat([1, 0], KANDIDAT, k=0)


def test_cari_terdekat_kandidat_kosong():
    assert vektor.cari_terdekat([1, 0], [], k=3) == []


def test_hasil_cari_tanpa_vektor():
    hasil = vektor.cari_terdekat([1, 0], KANDIDAT, k=1)

    assert set(hasil[0]) == {"teks", "topik", "skor"}


def test_precision_at_k():
    hasil = [
        {"topik": "teknologi"},
        {"topik": "kuliner"},
        {"topik": "teknologi"},
    ]

    assert vektor.precision_at_k(hasil, "teknologi", k=3) == pytest.approx(2 / 3)
    assert vektor.precision_at_k(hasil, "teknologi", k=2) == pytest.approx(1 / 2)


def test_precision_at_k_kosong():
    assert vektor.precision_at_k([], "teknologi") == 0.0


@pytest.mark.parametrize("k", [0, -1])
def test_precision_at_k_k_invalid(k):
    with pytest.raises(ValueError):
        vektor.precision_at_k([{"topik": "teknologi"}], "teknologi", k=k)
