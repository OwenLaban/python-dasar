# ============================================
# LATIHAN 12: FastAPI dasar — Notes API mini
# ============================================
# Jalankan dari folder python-dasar (venv aktif):
#   python -m uvicorn latihan_fastapi.main:app --reload
# Buka dokumentasi interaktif:
#   http://127.0.0.1:8000/docs
#
# Isi TODO di bawah, lalu uji lewat /docs atau pytest (latihan 13).
# ============================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Latihan FastAPI")


# --- Model: bentuk data yang diterima/dikirim ---
# Pydantic otomatis memvalidasi: kalau "judul" tidak dikirim -> 422.
class Catatan(BaseModel):
    judul: str
    isi: str = ""


# Penyimpanan sementara di memori (hilang kalau server restart).
# Di proyek #2 nanti kita ganti dengan file JSON / database.
catatan: list[dict] = []
next_id = 1


@app.get("/")
def root():
    return {"pesan": "API latihan jalan"}


# --- SOAL 1: GET /catatan -> semua catatan ---
# TODO: return seluruh list `catatan`.
# Uji di /docs atau: curl http://127.0.0.1:8000/catatan
@app.get("/catatan")
def get_catatan():
    return catatan

# --- SOAL 2: POST /catatan -> buat catatan baru ---
# TODO:
#   global next_id
#   baru = {"id": next_id, "judul": data.judul, "isi": data.isi}
#   catatan.append(baru)
#   next_id += 1
#   return baru
# Dekorator: @app.post("/catatan", status_code=201)
# (201 = Created, lebih tepat daripada 200 untuk pembuatan data)
@app.post("/catatan", status_code=201)
def create_catatan(data: Catatan):
    global next_id
    baru = {"id": next_id, "judul": data.judul, "isi": data.isi}
    catatan.append(baru)
    next_id += 1
    return baru

# --- SOAL 3: GET /catatan/{id} -> satu catatan ---
# TODO:
#   - cari catatan yang id-nya cocok
#   - kalau tidak ada:
#       raise HTTPException(status_code=404, detail="Catatan tidak ditemukan")
#   - kalau ada: return catatannya
# Petunjuk: id dari URL otomatis jadi int kalau ditulis `id: int`.

@app.get("/catatan/{id}")
def get_catatan_by_id(id: int):
    for cat in catatan:
        if cat["id"] == id:
            return cat
    raise HTTPException(status_code=404, detail="Catatan tidak ditemukan")

# --- SOAL 4: DELETE /catatan/{id} ---
# TODO:
#   - hapus catatan dengan id tersebut
#   - kalau tidak ada: 404
#   - kalau berhasil: 204 (tanpa body)
# Dekorator: @app.delete("/catatan/{id}", status_code=204)
@app.delete("/catatan/{id}", status_code=204)
def delete_catatan(id: int):
    global catatan
    for i, cat in enumerate(catatan):
        if cat["id"] == id:
            catatan.pop(i)
            return
    raise HTTPException(status_code=404, detail="Catatan tidak ditemukan")

# --- SOAL 5 (bonus): PUT /catatan/{id} ---
# TODO:
#   - update judul + isi
#   - 404 kalau tidak ada
#   - return data terbaru
@app.put("/catatan/{id}")
def update_catatan(id: int, data: Catatan):
    global catatan
    for i, cat in enumerate(catatan):
        if cat["id"] == id:
            catatan[i] = {"id": id, "judul": data.judul, "isi": data.isi}
            return catatan[i]
    raise HTTPException(status_code=404, detail="Catatan tidak ditemukan")