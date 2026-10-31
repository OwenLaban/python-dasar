"""Test fungsi context engineering. Tidak memanggil model atau jaringan."""

import tiktoken
import pytest

from latihan_context import konteks

ENC = tiktoken.get_encoding(konteks.ENCODING)


def test_hitung_token():
    assert konteks.hitung_token("") == 0
    assert konteks.hitung_token("Halo dunia") == len(ENC.encode("Halo dunia"))


def test_potong_token():
    teks = "satu dua tiga empat lima enam tujuh delapan sembilan sepuluh"
    ids = ENC.encode(teks)
    expected = [ENC.decode(ids[i : i + 4]) for i in range(0, len(ids), 3)]

    hasil = konteks.potong_token(teks, max_token=4, overlap=1)

    assert hasil == expected
    assert all(konteks.hitung_token(bagian) <= 4 for bagian in hasil)


def test_potong_token_kosong():
    assert konteks.potong_token("", max_token=10) == []


@pytest.mark.parametrize(
    "max_token, overlap",
    [
        (0, 0),
        (-1, 0),
        (4, 4),
        (4, 5),
        (4, -1),
    ],
)
def test_potong_token_validasi(max_token, overlap):
    with pytest.raises(ValueError):
        konteks.potong_token("contoh teks", max_token=max_token, overlap=overlap)


def test_anggaran_input():
    assert konteks.anggaran_input(4096, 512, 128) == 3456


def test_anggaran_input_habis():
    with pytest.raises(ValueError):
        konteks.anggaran_input(100, 80, 20)


def test_pilih_strategi():
    assert konteks.pilih_strategi(100, 100) == "stuff"
    assert konteks.pilih_strategi(101, 100) == "map_reduce"


def test_pilih_strategi_batas_invalid():
    with pytest.raises(ValueError):
        konteks.pilih_strategi(10, 0)


def test_pangkas_riwayat():
    pesan = [
        {"role": "user", "content": "pesan lama"},
        {"role": "assistant", "content": "balasan lama"},
        {"role": "user", "content": "pesan baru"},
    ]
    batas = konteks.hitung_token("balasan lama") + konteks.hitung_token("pesan baru")

    hasil = konteks.pangkas_riwayat(pesan, max_token=batas)

    assert [item["content"] for item in hasil] == ["balasan lama", "pesan baru"]


def test_pangkas_riwayat_memotong_pesan_terbaru():
    pesan = [{"role": "user", "content": "ini pesan yang sangat panjang sekali"}]

    hasil = konteks.pangkas_riwayat(pesan, max_token=3)

    assert len(hasil) == 1
    assert konteks.hitung_token(hasil[0]["content"]) <= 3


def test_pangkas_riwayat_kosong():
    assert konteks.pangkas_riwayat([], max_token=10) == []


def test_gabung_ringkasan():
    bagian = ["Ringkasan pertama.", "Ringkasan kedua."]
    lengkap = "Ringkasan pertama.\nRingkasan kedua."

    assert konteks.gabung_ringkasan(bagian, konteks.hitung_token(lengkap)) == lengkap


def test_gabung_ringkasan_memotong():
    hasil = konteks.gabung_ringkasan(
        ["Ini ringkasan yang cukup panjang untuk dipotong."],
        max_token=5,
    )

    assert hasil
    assert konteks.hitung_token(hasil) <= 5


def test_gabung_ringkasan_kosong():
    assert konteks.gabung_ringkasan([], max_token=10) == ""


def test_gabung_ringkasan_validasi():
    with pytest.raises(ValueError):
        konteks.gabung_ringkasan(["contoh"], max_token=0)
