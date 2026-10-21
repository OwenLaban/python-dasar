# ============================================
# LATIHAN 11: Consume API dengan `requests`
# ============================================
# Cara pakai:
#   1. Aktifkan venv:
#        .\.venv\Scripts\Activate.ps1
#      (atau langsung: .\.venv\Scripts\python.exe 11_api_requests.py)
#   2. Isi TODO, lalu jalankan:
#        python 11_api_requests.py
#
# Butuh koneksi internet. API yang dipakai gratis, tanpa API key:
#   - GitHub API  https://api.github.com
#   - Open-Meteo  https://api.open-meteo.com
# ============================================

import os

import requests
from dotenv import load_dotenv

load_dotenv()  # baca file .env ke environment

# --- Konsep cepat ---
# requests.get(url, params=..., headers=..., timeout=...) -> Response
#   r.status_code -> 200, 404, dst.
#   r.json()      -> body JSON yang sudah jadi dict/list Python
#   r.text        -> body mentah (string)
#
# Pola aman:
#   r = requests.get(url, timeout=10)    # SELALU pakai timeout
#   if r.status_code == 200:
#       data = r.json()
#   else:
#       print("Gagal:", r.status_code)
#
# API key JANGAN ditulis di kode. Simpan di .env (yang di-gitignore),
# lalu baca dengan os.getenv("NAMA_KEY").

# --- CONTOH: GET sederhana ---
r = requests.get("https://api.github.com/users/octocat", timeout=10)
print("Status:", r.status_code)
if r.status_code == 200:
    user = r.json()
    print("Nama:", user["name"])
    print("Repo publik:", user["public_repos"])


# --- SOAL 1: ambil data user GitHub ---
# TODO: pakai username dari environment:
#   username = os.getenv("GITHUB_USER", "octocat")
# lalu GET https://api.github.com/users/<username>, print:
#   - status code
#   - nama
#   - jumlah followers
# Uji default: nama "The Octocat" (followers bisa berubah).
username = os.getenv("GITHUB_USER", "octocat")
url = f"https://api.github.com/users/{username}"
r = requests.get(url, timeout=10)
print("Status:", r.status_code)
if r.status_code == 200:
    user = r.json()
    print("Nama:", user["name"])
    print("Followers:", user["followers"])

# --- SOAL 2: query params ---
# TODO: cari 5 repo Python paling banyak bintang:
#   GET https://api.github.com/search/repositories
#   params = {"q": "language:python", "sort": "stars",
#             "order": "desc", "per_page": 5}
# print nomor + nama repo + jumlah stars.
# Petunjuk: hasilnya ada di r.json()["items"] (list of dict);
# nama repo -> "full_name", jumlah star -> "stargazers_count".
url = "https://api.github.com/search/repositories"
params = {"q": "language:python", "sort": "stars", "order": "desc", "per_page": 5}
r = requests.get(url, params=params, timeout=10)
if r.status_code == 200:
    items = r.json()["items"]
    for i, repo in enumerate(items, start=1):
        print(f"{i}. {repo['full_name']} ({repo['stargazers_count']} stars)")

# --- SOAL 3: tangani 404 ---
# TODO: GET https://api.github.com/users/user-yang-tidak-ada-xyz
# JANGAN pakai raise_for_status; cek status_code:
#   - 200  -> print nama
#   - 404  -> print "User tidak ditemukan (404)"
#   - lain -> print "Error:", status_code
# Uji: harus masuk cabang 404, bukan crash.
url = "https://api.github.com/users/user-yang-tidak-ada-xyz"
r = requests.get(url, timeout=10)

if r.status_code == 200:
    user = r.json()
    print("Nama:", user["name"])
elif r.status_code == 404:
    print("User tidak ditemukan (404)")
else:
    print("Error:", r.status_code)

# --- SOAL 4: environment (.env) ---
# TODO:
#   1. buka file .env, ubah GITHUB_USER jadi namamu (atau user favorit)
#   2. jalankan lagi SOAL 1 -> hasilnya ikut berubah tanpa mengubah kode
# Ini inti environment variable: konfigurasi tanpa hardcode.
# (Kalau belum ada .env: copy dari .env.example)


# --- SOAL 5 (mini challenge): cuaca kota dari .env ---
# TODO:
#   1. baca WEATHER_CITY dari env (default "Jakarta")
#   2. geocoding:
#        GET https://geocoding-api.open-meteo.com/v1/search
#        params={"name": kota, "count": 1, "language": "id"}
#      -> ambil results[0]["latitude"] dan results[0]["longitude"]
#   3. cuaca:
#        GET https://api.open-meteo.com/v1/forecast
#        params={"latitude": lat, "longitude": lon,
#                "current": "temperature_2m"}
#      -> ambil current["temperature_2m"]
#   4. print: "Di <kota> sekarang <suhu> derajat C"
# Petunjuk: tangani kalau kota tidak ditemukan ("results" tidak ada).
url_geocode = "https://geocoding-api.open-meteo.com/v1/search"
kota = os.getenv("WEATHER_CITY", "Jakarta")
params_geocode = {"name": kota, "count": 1, "language": "id"}
r = requests.get(url_geocode, params=params_geocode, timeout=10)
if r.status_code == 200:
    data = r.json()
    if "results" in data and len(data["results"]) > 0:
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        url_weather = "https://api.open-meteo.com/v1/forecast"
        params_weather = {"latitude": lat, "longitude": lon, "current": "temperature_2m"}
        r_weather = requests.get(url_weather, params=params_weather, timeout=10)
        if r_weather.status_code == 200:
            weather_data = r_weather.json()
            suhu = weather_data["current"]["temperature_2m"]
            print(f"Di {kota} sekarang {suhu} derajat C")
        else:
            print("Gagal mendapatkan data cuaca:", r_weather.status_code)
    else:
        print(f"Kota '{kota}' tidak ditemukan.")