"""Test fungsi vector database. Tidak memanggil Chroma, Ollama, atau jaringan."""

import pytest

from latihan_vectordb import vektor_db
from latihan_vectordb.dokumen import build_dokumen


def buat_record(
    id: str,
    teks: str = "dokumen uji",
    kategori: str = "teknologi",
    level: str = "dasar",
    tahun: int = 2024,
    vektor: list[float] | None = None,
    **metadata_lain,
) -> dict:
    """Bantu membuat record siap pakai untuk test."""
    metadata = {
        "kategori": kategori,
        "level": level,
        "tahun": tahun,
        **metadata_lain,
    }
    return {
        "id": id,
        "teks": teks,
        "metadata": metadata,
        "vektor": vektor if vektor is not None else [1.0, 0.0],
    }


KANDIDAT = [
    buat_record("A", vektor=[1.0, 0.0]),
    buat_record("B", vektor=[0.8, 0.6]),
    buat_record("C", vektor=[0.0, 1.0], kategori="kuliner"),
]


# --- id_stabil -----------------------------------------------------------


def test_id_stabil_deterministik():
    assert vektor_db.id_stabil("python itu keren") == vektor_db.id_stabil(
        "python itu keren"
    )


def test_id_stabil_panjang_dan_hex():
    id_dokumen = vektor_db.id_stabil("python itu keren")

    assert len(id_dokumen) == 16
    assert all(char in "0123456789abcdef" for char in id_dokumen)


def test_id_stabil_berbeda_untuk_teks_berbeda():
    assert vektor_db.id_stabil("python") != vektor_db.id_stabil("javascript")


# --- normalisasi_metadata ------------------------------------------------


def test_normalisasi_metadata_field_diizinkan():
    hasil = vektor_db.normalisasi_metadata(
        {"kategori": "teknologi", "rahasia": "jangan simpan"}
    )

    assert hasil == {"kategori": "teknologi"}


def test_normalisasi_metadata_hapus_none():
    hasil = vektor_db.normalisasi_metadata(
        {"kategori": "teknologi", "sumber": None}
    )

    assert hasil == {"kategori": "teknologi"}


def test_normalisasi_metadata_gabung_list():
    hasil = vektor_db.normalisasi_metadata({"tag": ["python", "pemula"]})

    assert hasil == {"tag": "python, pemula"}


def test_normalisasi_metadata_tahun_jadi_int():
    hasil = vektor_db.normalisasi_metadata({"tahun": "2024"})

    assert hasil == {"tahun": 2024}
    assert isinstance(hasil["tahun"], int)


def test_normalisasi_metadata_kosong():
    assert vektor_db.normalisasi_metadata({}) == {}


# --- siapkan_koleksi -----------------------------------------------------


def test_siapkan_koleksi_jumlah_dan_field():
    dokumen = [
        {"id": "a", "teks": "teks a", "kategori": "teknologi"},
        {"id": "b", "teks": "teks b", "kategori": "keuangan"},
    ]

    hasil = vektor_db.siapkan_koleksi(dokumen)

    assert len(hasil) == 2
    assert set(hasil[0]) == {"id", "teks", "metadata"}


def test_siapkan_koleksi_id_dari_teks():
    hasil = vektor_db.siapkan_koleksi(
        [{"teks": "dokumen tanpa id", "kategori": "teknologi"}]
    )

    assert hasil[0]["id"] == vektor_db.id_stabil("dokumen tanpa id")


def test_siapkan_koleksi_id_duplikat_gagal():
    dokumen = [
        {"id": "sama", "teks": "teks a", "kategori": "teknologi"},
        {"id": "sama", "teks": "teks b", "kategori": "keuangan"},
    ]

    with pytest.raises(ValueError):
        vektor_db.siapkan_koleksi(dokumen)


def test_siapkan_koleksi_teks_kosong_gagal():
    with pytest.raises(ValueError):
        vektor_db.siapkan_koleksi([{"teks": "  ", "kategori": "teknologi"}])


def test_siapkan_koleksi_kategori_wajib_gagal():
    with pytest.raises(ValueError):
        vektor_db.siapkan_koleksi([{"teks": "teks tanpa kategori"}])


def test_siapkan_koleksi_metadata_tanpa_none():
    hasil = vektor_db.siapkan_koleksi(
        [{"id": "a", "teks": "teks a", "kategori": "teknologi", "sumber": None}]
    )

    assert hasil[0]["metadata"] == {"kategori": "teknologi"}


# --- filter_metadata -----------------------------------------------------


def test_filter_metadata_tanpa_filter():
    assert len(vektor_db.filter_metadata(KANDIDAT, None)) == 3
    assert len(vektor_db.filter_metadata(KANDIDAT, {})) == 3


def test_filter_metadata_sama_dengan():
    hasil = vektor_db.filter_metadata(KANDIDAT, {"kategori": "kuliner"})

    assert [item["id"] for item in hasil] == ["C"]


def test_filter_metadata_salah_satu_dari():
    hasil = vektor_db.filter_metadata(
        KANDIDAT, {"level": {"$in": ["dasar", "menengah"]}}
    )

    assert [item["id"] for item in hasil] == ["A", "B"]


def test_filter_metadata_bukan():
    hasil = vektor_db.filter_metadata(KANDIDAT, {"level": {"$ne": "dasar"}})

    assert hasil == []


def test_filter_metadata_gabungan():
    hasil = vektor_db.filter_metadata(
        KANDIDAT, {"kategori": "teknologi", "tahun": 2024}
    )

    assert [item["id"] for item in hasil] == ["A", "B"]


def test_filter_metadata_tidak_ada_hasil():
    assert vektor_db.filter_metadata(KANDIDAT, {"kategori": "tidak-ada"}) == []


def test_filter_metadata_operator_asing_gagal():
    with pytest.raises(ValueError):
        vektor_db.filter_metadata(KANDIDAT, {"level": {"$like": "das%"}})


# --- cari_semantik ------------------------------------------------------


def test_cari_semantik_urutan_skor():
    hasil = vektor_db.cari_semantik([1.0, 0.0], KANDIDAT, k=3)

    assert [item["id"] for item in hasil] == ["A", "B", "C"]
    assert hasil[0]["skor"] == pytest.approx(1.0)
    assert hasil[1]["skor"] == pytest.approx(0.8)


def test_cari_semantik_batasi_k():
    hasil = vektor_db.cari_semantik([1.0, 0.0], KANDIDAT, k=2)

    assert len(hasil) == 2
    assert [item["id"] for item in hasil] == ["A", "B"]


def test_cari_semantik_k_invalid():
    with pytest.raises(ValueError):
        vektor_db.cari_semantik([1.0, 0.0], KANDIDAT, k=0)


def test_cari_semantik_filter_dilakukan():
    hasil = vektor_db.cari_semantik(
        [1.0, 0.0], KANDIDAT, k=3, where={"kategori": "kuliner"}
    )

    assert [item["id"] for item in hasil] == ["C"]


def test_cari_semantik_dimensi_salah_gagal():
    with pytest.raises(ValueError):
        vektor_db.cari_semantik([1.0, 0.0, 0.0], KANDIDAT, k=3)


def test_cari_semantik_field_hasil():
    hasil = vektor_db.cari_semantik([1.0, 0.0], KANDIDAT, k=1)

    assert set(hasil[0]) == {"id", "teks", "metadata", "skor"}


# --- statistik_koleksi ---------------------------------------------------


def test_statistik_koleksi():
    dokumen = [
        buat_record("A", kategori="teknologi", level="dasar"),
        buat_record("B", kategori="teknologi", level="lanjut"),
        buat_record("C", kategori="kuliner", level="dasar"),
    ]

    hasil = vektor_db.statistik_koleksi(dokumen)

    assert hasil["total"] == 3
    assert hasil["per_kategori"] == {"teknologi": 2, "kuliner": 1}
    assert hasil["per_level"] == {"dasar": 2, "lanjut": 1}
    assert hasil["dimensi"] == 2


# --- dataset -------------------------------------------------------------


def test_dokumen_100_dan_id_unik():
    dokumen = build_dokumen()

    assert len(dokumen) == 100
    assert len({item["id"] for item in dokumen}) == 100


def test_dokumen_metadata_variasi():
    dokumen = build_dokumen()

    assert len({item["kategori"] for item in dokumen}) == 5
    assert len({item["level"] for item in dokumen}) == 3
    assert len({item["tahun"] for item in dokumen}) == 3
    assert all(isinstance(item["tag"], list) for item in dokumen)
