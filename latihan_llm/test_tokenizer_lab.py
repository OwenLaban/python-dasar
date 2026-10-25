# ============================================
# LATIHAN 14: Test tokenizer
# ============================================
# Jalankan dari folder python-dasar (venv aktif):
#   pytest latihan_llm -v
# ============================================

import latihan_llm.tokenizer_lab as lab

TEKS_A = "Halo, saya sedang belajar menjadi AI Engineer."
TEKS_B = "Hello, I am learning to become an AI Engineer."


def test_hitung_token():
    assert lab.hitung_token("Halo") == 1
    assert lab.hitung_token(TEKS_A) == 9
    assert lab.hitung_token(TEKS_B) == 11


def test_pecah_token():
    assert lab.pecah_token("kemerdekaan") == ["kem", "erde", "kaan"]
    assert len(lab.pecah_token("ketidaksempurnaan")) == 6


def test_pecah_token_mengikuti_encoding():
    assert len(lab.pecah_token("kemerdekaan", encoding="o200k_base")) == 3
    assert len(lab.pecah_token("kemerdekaan", encoding="cl100k_base")) == 5


def test_bandingkan():
    hasil = lab.bandingkan(TEKS_A, TEKS_B)
    assert hasil["token_a"] == 9
    assert hasil["token_b"] == 11
    assert hasil["selisih"] == 2
    assert hasil["lebih_boros"] == "B"

    sama = lab.bandingkan("Halo", "Halo")
    assert sama["lebih_boros"] == "sama"
    assert sama["selisih"] == 0


def test_muat_dalam_context():
    assert lab.muat_dalam_context(TEKS_A, 9) is True
    assert lab.muat_dalam_context(TEKS_A, 8) is False
