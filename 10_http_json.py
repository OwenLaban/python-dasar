# ============================================
# LATIHAN 10: HTTP & JSON
# ============================================
# Cara pakai: isi bagian yang masih kosong, lalu jalankan:
#   python 10_http_json.py
# Target: paham istilah HTTP + bisa olah JSON dengan modul `json`.
# ============================================

# --- Konsep: HTTP dalam 1 menit ---
# API = pintu untuk program lain bicara ke sebuah layanan lewat HTTP.
# Satu interaksi = request (kita kirim) + response (server balas).
#
# Request punya:
#   method    = maksud kita:
#               GET       -> ambil data
#               POST      -> buat data baru
#               PUT/PATCH -> ubah data
#               DELETE    -> hapus data
#   URL/path  = alamat resource, mis. /users/octocat
#   headers   = info tambahan, mis. Authorization: Bearer <token>
#   body      = data yang dikirim (biasanya JSON) — untuk POST/PUT
#
# Response punya:
#   status code = hasil singkat:
#               2xx sukses  (200 OK, 201 Created)
#               3xx redirect
#               4xx salah di sisi client
#                   (400 Bad Request, 401 Unauthorized, 403 Forbidden,
#                    404 Not Found, 429 Too Many Requests)
#               5xx salah di sisi server (500 Internal Server Error)
#   headers     = info tambahan (Content-Type, rate limit, dll.)
#   body        = datanya, biasanya JSON
#
# JSON = format teks untuk data terstruktur, bentuknya mirip dict/list Python:
#   {"nama": "Wenn", "umur": 22, "hobi": ["coding", "baca"], "aktif": true}
# Bedanya: true/false/null (Python: True/False/None), dan key selalu string.

import json

# --- CONTOH: json.loads dan json.dumps ---
contoh = '{"nama": "Wenn", "aktif": true}'
data = json.loads(contoh)          # teks JSON -> dict
print(data["nama"])                # Wenn
print(json.dumps(data, indent=2))  # dict -> teks JSON rapi


# --- SOAL 1: JSON string -> dict ---
# TODO:
#   data_teks = '{"nama": "Wenn", "umur": 22, "kota": "Bandung"}'
#   ubah ke dict dengan json.loads, lalu print nilai "nama"
# Uji: Wenn
data_teks = '{"nama": "Wenn", "umur": 22, "kota": "Bandung"}'
data_dict = json.loads(data_teks)
print(data_dict["nama"])  # Output: Wenn
# --- SOAL 2: dict -> JSON string ---
# TODO: buat dict mahasiswa = {"nama": ..., "umur": ..., "aktif": True}
# lalu print json.dumps(mahasiswa, indent=2)
# Perhatikan: True jadi true, dan hasilnya berupa string.
mahasiswa = {"nama": "Wenn", "umur": 22, "aktif": True}
json_string = json.dumps(mahasiswa, indent=2)
print(json_string)

# --- SOAL 3: JSON bersarang ---
# TODO: dari JSON ini, ambil nama repo pertama dan jumlah starnya:
respons = '{"items": [{"nama": "repo-a", "stars": 120}, {"nama": "repo-b", "stars": 45}]}'
# Petunjuk: json.loads dulu -> ["items"] -> [0] -> ["nama"] / ["stars"]
# Uji: "repo pertama: repo-a (120 stars)"
respons_dict = json.loads(respons)
repo_pertama = respons_dict["items"][0]
print(f'repo pertama: {repo_pertama["nama"]} ({repo_pertama["stars"]} stars)')
# --- SOAL 4: olah list of dict ---
tugas = [
    {"teks": "Belajar HTTP", "selesai": True},
    {"teks": "Latihan JSON", "selesai": False},
    {"teks": "Baca status code", "selesai": False},
]
# TODO: print teks tugas yang BELUM selesai saja
# Uji: Latihan JSON / Baca status code
# Bonus: hitung berapa tugas yang sudah selesai.
tugas_belum_selesai = [t["teks"] for t in tugas if not t["selesai"]]
print("Tugas yang belum selesai:")
for teks in tugas_belum_selesai:
    print(f" - {teks}")

tugas_selesai = len(tugas) - len(tugas_belum_selesai)
print(f"Jumlah tugas yang sudah selesai: {tugas_selesai}")

# --- SOAL 5: status code (tanpa komputer) ---
# Tebak status code yang paling tepat untuk situasi berikut:
#   a) GET /users/tidak-ada-yang-ini   -> 404
#   b) GET /profil tanpa token         -> 401
#   c) GET berhasil                    -> 200
#   d) server crash                    -> 500
# Kunci: 404, 401, 200, 500 — cek setelah kamu menjawab sendiri.
