# 🐍 python-dasar

Latihan dasar Python + proyek CLI — Minggu 1–2 dari perjalanan belajar AI Engineer 24 minggu ([roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)).

## Isi Latihan

| File | Materi |
| --- | --- |
| `01_variabel_typedata.py` | Variabel, tipe data (int/float/str/bool), f-string, konversi tipe, `input()` |
| `02_list_dict_loop.py` | List, dict, `for` loop, `enumerate`, total & rata-rata, cari nilai tertinggi |
| `03_fungsi.py` | Fungsi, parameter, `return`, default parameter, `if/else` |
| `04_kalkulator_konversi.py` | **Proyek Minggu 1:** kalkulator interaktif + konverter suhu (C → F, C → K) |
| `05_error_handling.py` | Error handling: `try/except`, `raise`, multiple exception |
| `06_file_io_modul.py` | Baca/tulis file, `with`, modul (`math`, `datetime`) |
| `07_oop.py` | OOP: class, `__init__`, method, inheritance, `__str__` |
| `08_sintaks_modern.py` | f-string format, list comprehension, type hints |
| `09_manajemen_tugas.py` | **Proyek Minggu 2:** CLI manajemen tugas + JSON persistence |
| `10_http_json.py` | HTTP & JSON: method, status code, `json.loads`, `json.dumps` |
| `11_api_requests.py` | Consume API dengan `requests` + environment variable dari `.env` |

## Cara Menjalankan

Butuh Python 3.12+ (dikembangkan dengan Python 3.13.5).

Latihan 01–09 hanya memakai standard library. Untuk latihan 10–11, install
dependensi dulu:

```sh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Lalu jalankan:

```sh
python 04_kalkulator_konversi.py
python 09_manajemen_tugas.py
python 11_api_requests.py
```

Beberapa latihan meminta input secara interaktif, jadi jalankan langsung di terminal.

## Proyek 09 — Manajemen Tugas

Menu CLI untuk mengelola tugas sehari-hari. Data disimpan otomatis ke
`tugas.json` (satu folder dengan script) sehingga tidak hilang saat program
ditutup.

```text
===== MANAJEMEN TUGAS =====
1. Lihat tugas
2. Tambah tugas
3. Tandai selesai
4. Hapus tugas
5. Keluar
Pilih menu (1-5): 1
1. [x] Belajar OOP
2. [ ] Latihan file I/O
```

## Contoh Output — Proyek Kalkulator

```text
=====KALKULATOR=====
1. Tambah
2. Kurang
3. Kali
4. Bagi
5. C -> F
6. C -> K
7. Keluar
Pilih = 5
Input Nilai suhu : 100
Hasil = 212.0
```

## Materi yang Sudah Dikuasai

- **Dasar:** variabel & 4 tipe data, f-string, konversi tipe (`int()`, `float()`)
- **Struktur data:** list (indeks, `append`, `len`), dict (akses key, tambah key baru)
- **Loop:** `for`, `enumerate`, akumulasi manual, pencarian nilai ekstrem
- **Fungsi:** parameter, `return` vs `print`, default parameter, `if/else`
- **Error handling:** `try/except`, `raise`, `except ... as e`
- **File I/O:** `open` mode `r`/`w`/`a`, `with`, modul `json`
- **OOP:** class, `__init__`, attribute, method, inheritance, `__str__`
- **Sintaks modern:** format spec f-string, list comprehension, type hints
