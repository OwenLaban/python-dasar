"""Implementasi vector database sederhana, langkah demi langkah.

Vector database sungguhan (Chroma, Qdrant, pgvector) melakukan tiga hal:

1. menyimpan embedding beserta metadata;
2. membangun index untuk mencari tetangga terdekat dengan cepat;
3. memfilter berdasarkan metadata sebelum atau sesudah pencarian.

Di sini kita versi sederhana dan bisa dibaca: semua data ditahan di memori,
pencarian dibandingkan langsung satu per satu (brute force), dan filter
metadata dijalankan manual. Setelah fungsinya jadi, kita bandingkan hasilnya
dengan Chroma di `eksperimen_vectordb.py`.
"""

import hashlib

from latihan_embedding import vektor

FIELD_METADATA = {
    "kategori": str,
    "level": str,
    "tahun": int,
    "sumber": str,
    "tag": str,
}

OPERATOR_DIDUKUNG = {"$eq", "$in", "$ne"}


def id_stabil(teks: str) -> str:
    """Buat ID 16 karakter heksadesimal yang sama untuk teks yang sama.

    Vector database butuh ID unik dan stabil: kalau dokumen yang sama
    di-index dua kali, ID-nya harus sama supaya dokumen itu diperbarui,
    bukan diduplikasi.

    TODO:
    1. Hitung hash SHA-256 dari ``teks`` dalam UTF-8.
    2. Ambil 16 karakter pertama heksadesimalnya.
    """
    raise NotImplementedError("TODO: implementasikan id_stabil()")


def normalisasi_metadata(dokumen: dict) -> dict:
    """Bersihkan metadata: hanya field yang diizinkan, tanpa ``None``, tanpa list.

    Aturan:
    - key di luar ``FIELD_METADATA`` dibuang;
    - nilai ``None`` dibuang;
    - nilai list/tuple/set digabung menjadi string dengan pemisah ``", "``;
    - ``tahun`` dikonversi ke int bila bisa;
    - nilai lain dikonversi ke str.

    TODO: kerjakan sesuai aturan di atas.
    """
    raise NotImplementedError("TODO: implementasikan normalisasi_metadata()")


def siapkan_koleksi(dokumen: list[dict]) -> list[dict]:
    """Validasi dan normalisasi dokumen menjadi record siap simpan.

    Setiap record hasil fungsi ini punya tepat tiga field: ``id``, ``teks``,
    dan ``metadata``. Field ``vektor`` ditambahkan nanti oleh skrip eksperimen.

    Aturan:
    - ``teks`` wajib ada dan tidak boleh kosong;
    - ``kategori`` wajib ada dan tidak boleh kosong;
    - ``id`` memakai ``dokumen["id"]`` bila ada, jika tidak pakai
      ``id_stabil(teks)``;
    - ID duplikat harus raise ``ValueError``.

    TODO: implementasikan.
    """
    raise NotImplementedError("TODO: implementasikan siapkan_koleksi()")


def filter_metadata(dokumen: list[dict], where: dict | None) -> list[dict]:
    """Filter dokumen berdasarkan metadata.

    Format ``where``:

    ```text
    {"kategori": "teknologi"}                     # sama dengan
    {"level": {"$in": ["dasar", "menengah"]}}      # salah satu dari
    {"level": {"$ne": "lanjut"}}                   # bukan
    {"kategori": "teknologi", "tahun": 2024}      # semua syarat harus cocok
    ```

    ``where`` None atau ``{}`` berarti semua dokumen lolos.
    Key yang tidak ada pada metadata menyebabkan dokumen tidak cocok.

    TODO: implementasikan.
    """
    raise NotImplementedError("TODO: implementasikan filter_metadata()")


def cari_semantik(
    query_vec: list[float],
    dokumen: list[dict],
    k: int = 3,
    where: dict | None = None,
) -> list[dict]:
    """Cari ``k`` dokumen paling mirip dengan query.

    Urutan proses: filter metadata dulu, lalu bandingkan cosine similarity
    dengan setiap dokumen, lalu ambil ``k`` teratas.

    Record harus punya field ``vektor``. Hasil returned punya ``id``, ``teks``,
    ``metadata``, dan ``skor``.

    TODO:
    1. Validasi ``k > 0``.
    2. Filter dengan ``filter_metadata``.
    3. Hitung cosine similarity (pakai ``latihan_embedding.vektor``).
    4. Urutkan skor tertinggi, ambil ``k`` teratas.
    """
    raise NotImplementedError("TODO: implementasikan cari_semantik()")


def statistik_koleksi(dokumen: list[dict]) -> dict:
    """Ringkasan koleksi: total, jumlah per kategori, jumlah per level, dimensi.

    Dimensi diambil dari panjang ``vektor`` dokumen pertama. Bila dokumen
    belum punya vektor, dimensi bernilai ``None``.

    TODO: implementasikan.
    """
    raise NotImplementedError("TODO: implementasikan statistik_koleksi()")
