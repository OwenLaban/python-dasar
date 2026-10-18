# 🐍 python-dasar

Latihan dasar Python — Minggu 1 dari perjalanan belajar AI Engineer 24 minggu ([roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)).

## Isi Latihan

| File | Materi |
| --- | --- |
| `01_variabel_typedata.py` | Variabel, tipe data (int/float/str/bool), f-string, konversi tipe, `input()` |
| `02_list_dict_loop.py` | List, dict, `for` loop, `enumerate`, total & rata-rata, cari nilai tertinggi |
| `03_fungsi.py` | Fungsi, parameter, `return`, default parameter, `if/else` |
| `04_kalkulator_konversi.py` | **Proyek utama:** kalkulator interaktif + konverter suhu (C → F, C → K) |

## Cara Menjalankan

Butuh Python 3.12+ (dikembangkan dengan Python 3.13.5).

```sh
python 04_kalkulator_konversi.py
```

Beberapa latihan meminta input secara interaktif, jadi jalankan langsung di terminal.

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

- Variabel & 4 tipe data dasar, f-string, konversi tipe (`int()`, `float()`)
- List (indeks, `append`, `len`), dict (akses key, tambah key baru)
- Loop: `for`, `enumerate`, akumulasi manual, pencarian nilai ekstrem
- Fungsi: parameter, `return` vs `print`, default parameter, kondisi `if/else`
- Struktur program: `while` loop + menu + `break`, penanganan pembagian nol (`None`)
