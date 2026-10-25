# Latihan 14 — Tokenizer & Context Window

Tujuan: membuktikan sendiri bahwa **token ≠ kata** dan bahwa tokenizer memecah
teks berdasarkan vocabulary model.

Status: ✅ selesai — 5/5 test lulus.

## Prasyarat

Dari folder `python-dasar`, dengan venv aktif:

```powershell
pip install -r requirements.txt
```

`tiktoken` sudah ditambahkan ke `requirements.txt`.

## File

```text
latihan_llm/
├── tokenizer_lab.py       # 4 fungsi TODO yang harus kamu lengkapi
├── test_tokenizer_lab.py  # test untuk mengecek hasil
├── jawaban.md             # lembar observasi yang kamu isi
└── __init__.py
```

## TODO

Lengkapi 4 fungsi di `tokenizer_lab.py`:

1. `hitung_token()` — jumlah token dari sebuah teks.
2. `pecah_token()` — daftar potongan token, misal `['kem', 'erde', 'kaan']`.
3. `bandingkan()` — bandingkan jumlah token dua teks.
4. `muat_dalam_context()` — cek apakah teks muat dalam batas token.

Gunakan `tiktoken.get_encoding(encoding)`, lalu method `.encode()` dan `.decode()`.
Jangan lupa: satu id token di-decode sebagai list, misal `enc.decode([id])`.

## Jalankan

```powershell
# dari folder python-dasar
python -m latihan_llm.tokenizer_lab
pytest latihan_llm -v
```

Target: **5 test lulus**.

## Setelah lulus

1. Isi `jawaban.md` berdasarkan hasil script.
2. Commit latihan ini.
3. Bandingkan hasilmu dengan temuan di tokenizer playground — angkanya bisa
   berbeda kalau encoding/model yang dipakai berbeda.
