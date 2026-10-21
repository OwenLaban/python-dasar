# ============================================
# LATIHAN 13: Test API dengan pytest
# ============================================
# Jalankan dari folder python-dasar (venv aktif):
#   pytest latihan_fastapi -v
#
# Isi TODO test di bawah. Dua test pertama sudah jadi contoh.
# ============================================

from fastapi.testclient import TestClient

import latihan_fastapi.main as main

client = TestClient(main.app)


def setup_function():
    """Reset data sebelum SETIAP test supaya test tidak saling mempengaruhi."""
    main.catatan.clear()
    main.next_id = 1


# --- CONTOH: test endpoint root ---
def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["pesan"] == "API latihan jalan"


# --- CONTOH: test list kosong ---
def test_get_catatan_kosong():
    r = client.get("/catatan")
    assert r.status_code == 200
    assert r.json() == []


# --- SOAL 1: test POST /catatan ---
# TODO:
#   r = client.post("/catatan", json={"judul": "Test", "isi": "Isi test"})
#   assert r.status_code == 201
#   hasil = r.json()
#   assert hasil["judul"] == "Test"
#   assert "id" in hasil


# --- SOAL 2: test GET /catatan/{id} ---
# TODO:
#   - buat 1 catatan lewat POST, ambil id-nya
#   - GET /catatan/{id}
#   - assert 200 dan judulnya sama


# --- SOAL 3: test 404 ---
# TODO:
#   - GET /catatan/999 -> assert 404
#   - DELETE /catatan/999 -> assert 404


# --- SOAL 4: test DELETE ---
# TODO:
#   - buat catatan, lalu DELETE -> assert 204
#   - GET catatan yang sama -> assert 404


# --- SOAL 5: test validasi Pydantic ---
# TODO:
#   - POST /catatan dengan json={"isi": "tanpa judul"}
#   - assert 422 (judul wajib diisi)
