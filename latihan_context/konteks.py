"""Fungsi dasar untuk mengelola konteks LLM.

Semua fungsi di sini bekerja pada level token, bukan sekadar jumlah kata.
Token adalah unit yang benar-benar dihitung oleh model.
"""

import tiktoken

ENCODING = "o200k_base"


def hitung_token(teks: str, encoding: str = ENCODING) -> int:
    """Kembalikan jumlah token dari sebuah teks."""
    encoder = tiktoken.get_encoding(encoding)
    encoded = encoder.encode(teks)
    return len(encoded)


def potong_token(
    teks: str,
    max_token: int,
    overlap: int = 0,
    encoding: str = ENCODING,
) -> list[str]:
    """Potong teks menjadi beberapa bagian berdasarkan token.

    Aturan:
    - ``max_token`` harus > 0.
    - ``overlap`` harus >= 0 dan < ``max_token``.
    - Teks kosong menghasilkan list kosong.
    - Setiap potongan berisi paling banyak ``max_token`` token.
    - Potongan berikutnya memakai ``max_token - overlap`` token sebelumnya
      sebagai konteks tambahan, supaya informasi di batas potongan tidak hilang.

    Petunjuk: encode seluruh teks lebih dulu, lalu potong daftar token ID.
    Setelah itu decode setiap potongan kembali menjadi string.
    """
    if max_token <= 0:
        raise ValueError("max_token harus > 0")
    if overlap < 0 or overlap >= max_token:
        raise ValueError("overlap harus >= 0 dan < max_token")
    if not teks:
        return []

    encoder = tiktoken.get_encoding(encoding)
    token_ids = encoder.encode(teks)

    potongan = []
    start = 0
    while start < len(token_ids):
        end = min(start + max_token, len(token_ids))
        potongan_ids = token_ids[start:end]
        potongan_teks = encoder.decode(potongan_ids)
        potongan.append(potongan_teks)
        start += max_token - overlap

    return potongan


def anggaran_input(
    batas_konteks: int,
    token_output: int,
    token_sistem: int = 0,
) -> int:
    """Hitung token yang tersedia untuk input setelah menyisihkan output.

    Rumus: ``batas_konteks - token_output - token_sistem``.
    Jika hasilnya <= 0, raise ``ValueError`` karena tidak ada ruang untuk input.
    """
    sisa = batas_konteks - token_output - token_sistem
    if sisa <= 0:
        raise ValueError("Tidak ada ruang untuk input: anggaran <= 0")
    return sisa


def pilih_strategi(jumlah_token: int, batas_input: int) -> str:
    """Pilih strategi ringkasan berdasarkan ukuran input.

    - ``"stuff"`` jika seluruh teks muat dalam ``batas_input``.
    - ``"map_reduce"`` jika tidak muat.

    Raise ``ValueError`` jika ``batas_input`` <= 0.
    """
    if batas_input <= 0:
        raise ValueError("batas_input harus > 0")
    return "stuff" if jumlah_token <= batas_input else "map_reduce"


def pangkas_riwayat(
    pesan: list[dict],
    max_token: int,
    encoding: str = ENCODING,
) -> list[dict]:
    """Pertahankan pesan terbaru yang muat dalam anggaran token.

    Setiap item pesan diasumsikan memiliki field ``content``.
    Mulai dari pesan paling baru, lalu ambil pesan sebelumnya selama masih muat.
    Jika pesan berikutnya tidak muat seluruhnya, potong isinya sesuai sisa
    anggaran, lalu berhenti. Kembalikan pesan dalam urutan kronologis semula.

    Ini adalah bentuk sederhana **compaction**: model tidak perlu melihat
    seluruh riwayat jika anggaran token sudah habis.

    Raise ``ValueError`` jika ``max_token`` <= 0.
    """
    if max_token <= 0:
        raise ValueError("max_token harus > 0")

    encoder = tiktoken.get_encoding(encoding)
    sisa_token = max_token
    pesan_terpangkas = []

    for item in reversed(pesan):
        if sisa_token <= 0:
            break
        content = item.get("content", "")
        token_count = len(encoder.encode(content))

        if token_count <= sisa_token:
            pesan_terpangkas.append(item)
            sisa_token -= token_count
        else:
            # Potong konten sesuai sisa token
            potongan_ids = encoder.encode(content)[:sisa_token]
            potongan_content = encoder.decode(potongan_ids)
            pesan_terpangkas.append({**item, "content": potongan_content})
            break

    return list(reversed(pesan_terpangkas))


def gabung_ringkasan(
    ringkasan: list[str],
    max_token: int,
    encoding: str = ENCODING,
) -> str:
    """Gabungkan beberapa ringkasan menjadi satu, dengan batas token.

    Ringkasan digabung dengan newline. Jika ringkasan berikutnya tidak muat,
    potong bagian itu sesuai sisa anggaran lalu berhenti. Token newline ikut
    dihitung agar hasil tidak melewati ``max_token``.
    """
    if max_token <= 0:
        raise ValueError("max_token harus > 0")

    hasil = ""
    for bagian in ringkasan:
        calon = f"{hasil}\n{bagian}" if hasil else bagian

        if hitung_token(calon, encoding) <= max_token:
            hasil = calon
        else:
            potongan = potong_token(calon, max_token, encoding=encoding)
            hasil = potongan[0] if potongan else ""
            break

    return hasil


def main() -> None:
    teks = (
        "Context engineering adalah cara menyusun informasi yang masuk ke "
        "model. Kita perlu menghitung token, memilih sumber yang relevan, "
        "dan memadatkan riwayat agar model tidak kehilangan detail penting."
    )

    jumlah = hitung_token(teks)
    print(f"Token: {jumlah}")
    print(f"Potongan 8 token, overlap 2: {potong_token(teks, 8, 2)}")
    print(f"Anggaran input: {anggaran_input(2048, 256, 100)} token")
    print(f"Strategi: {pilih_strategi(jumlah, 20)}")


if __name__ == "__main__":
    main()
