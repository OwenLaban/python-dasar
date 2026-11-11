"""Eksperimen vector database: Chroma vs implementasi naive.

Jalankan setelah semua fungsi di ``vektor_db.py`` lulus test:

    .\\.venv\\Scripts\\python.exe -m latihan_vectordb.eksperimen_vectordb

Yang diukur:

1. indexing 100 dokumen ke Chroma (lokal, persistent);
2. 6 query semantic, dibandingkan antara implementasi naive (brute force)
   dan Chroma (index HNSW);
3. metadata filter pada Chroma;
4. operasi tambah, perbarui (upsert), dan hapus.
"""

import argparse
import json
import time
from pathlib import Path

from latihan_embedding.klien_embedding import EmbeddingClient, EmbeddingError
from latihan_vectordb import vektor_db
from latihan_vectordb.dokumen import QUERY, build_dokumen
from latihan_vectordb.klien_chroma import KoleksiChroma

MODEL_DEFAULT = "bge-m3"
K_DEFAULT = 3


def hitung_presisi(hasil: list[dict], kategori: str, k: int) -> float:
    """Proporsi hasil teratas yang kategorinya sesuai."""
    if not hasil:
        return 0.0

    teratas = hasil[:k]
    cocok = sum(
        1 for item in teratas if item.get("metadata", {}).get("kategori") == kategori
    )
    return cocok / len(teratas)


def jalankan(model: str, k: int, path: Path) -> dict:
    client = EmbeddingClient(model=model)

    try:
        terpasang = client.daftar_model()
    except EmbeddingError as error:
        raise SystemExit(f"Error: {error}") from error

    if not any(nama.startswith(model) for nama in terpasang):
        raise SystemExit(
            f"Model {model!r} belum terpasang. Jalankan: ollama pull {model}"
        )

    print(f"Model: {model}")
    print(f"Jalur database: {path}")

    dokumen = build_dokumen()
    print(f"Dokumen: {len(dokumen)}")

    record = vektor_db.siapkan_koleksi(dokumen)

    print("Membuat embedding ...", flush=True)
    mulai = time.perf_counter()
    try:
        vektor_dokumen = client.embed([item["teks"] for item in record])
        vektor_query = client.embed([item["teks"] for item in QUERY])
    except EmbeddingError as error:
        raise SystemExit(f"Error: {error}") from error
    waktu_embedding = time.perf_counter() - mulai

    for item, vec in zip(record, vektor_dokumen):
        item["vektor"] = vec

    dimensi = len(vektor_dokumen[0])
    print(f"Dimensi: {dimensi}")
    print(f"Waktu embedding: {waktu_embedding:.2f} s")

    # --- indexing ke Chroma ---
    koleksi = KoleksiChroma(path=path)
    koleksi.reset()

    mulai = time.perf_counter()
    koleksi.tambah(
        ids=[item["id"] for item in record],
        teks=[item["teks"] for item in record],
        vektor=[item["vektor"] for item in record],
        metadata=[item["metadata"] for item in record],
    )
    waktu_indexing = time.perf_counter() - mulai

    print(f"Dokumen di Chroma: {koleksi.jumlah()}")
    print(f"Waktu indexing: {waktu_indexing:.2f} s")

    # --- query: naive vs Chroma ---
    # Warm-up: panggilan pertama ke Chroma masih memuat inisialisasi index,
    # jadi angkanya tidak sebanding dengan panggilan berikutnya.
    koleksi.cari(vektor_query[0], k=k)

    hasil_query = []
    total_naive = 0.0
    total_chroma = 0.0

    for item, vec in zip(QUERY, vektor_query):
        query_vec = vec

        mulai = time.perf_counter()
        naive = vektor_db.cari_semantik(query_vec, record, k=k)
        waktu_naive = time.perf_counter() - mulai

        mulai = time.perf_counter()
        chroma = koleksi.cari(query_vec, k=k)
        waktu_chroma = time.perf_counter() - mulai

        total_naive += waktu_naive
        total_chroma += waktu_chroma

        presisi_naive = hitung_presisi(naive, item["kategori"], k)
        presisi_chroma = hitung_presisi(chroma, item["kategori"], k)

        hasil_query.append(
            {
                "query": item["teks"],
                "kategori_target": item["kategori"],
                "presisi_naive": round(presisi_naive, 4),
                "presisi_chroma": round(presisi_chroma, 4),
                "waktu_naive_ms": round(waktu_naive * 1000, 3),
                "waktu_chroma_ms": round(waktu_chroma * 1000, 3),
                "top_naive": [
                    {
                        "id": hasil_item["id"],
                        "kategori": hasil_item["metadata"].get("kategori"),
                        "skor": round(hasil_item["skor"], 4),
                        "teks": hasil_item["teks"],
                    }
                    for hasil_item in naive
                ],
                "top_chroma": [
                    {
                        "id": hasil_item["id"],
                        "kategori": hasil_item["metadata"].get("kategori"),
                        "skor": round(hasil_item["skor"], 4),
                        "teks": hasil_item["teks"],
                    }
                    for hasil_item in chroma
                ],
            }
        )

        print(f"\nQuery: {item['teks']}")
        for nomor, hasil_item in enumerate(chroma, start=1):
            print(
                f"  {nomor}. [{hasil_item['skor']:.3f}] "
                f"({hasil_item['metadata'].get('kategori')}) {hasil_item['teks']}"
            )
        print(f"  presisi@{k} naive: {presisi_naive:.2f} | chroma: {presisi_chroma:.2f}")

    # --- metadata filter ---
    demo_filter = []
    for nama, where in (
        ("kategori = keuangan", {"kategori": "keuangan"}),
        ("level in [dasar, menengah]", {"level": {"$in": ["dasar", "menengah"]}}),
        ("tahun >= 2024", {"tahun": {"$gte": 2024}}),
    ):
        hasil = koleksi.cari(vektor_query[0], k=5, where=where)
        demo_filter.append(
            {
                "filter": nama,
                "where": where,
                "jumlah_hasil": len(hasil),
                "kategori": sorted(
                    {item["metadata"].get("kategori") for item in hasil}
                ),
            }
        )
        print(f"\nFilter {nama}: {len(hasil)} hasil")

    # --- tambah, perbarui, hapus ---
    indeks = {item["id"]: nomor for nomor, item in enumerate(record)}
    teks_baru = "Rencana keuangan pribadi disusun setiap awal bulan."

    sebelum = koleksi.jumlah()
    koleksi.perbarui(
        ids=["keu-01"],
        teks=[teks_baru],
        vektor=[client.embed_satu(teks_baru)],
        metadata=[{"kategori": "keuangan", "level": "dasar", "tahun": 2025}],
    )
    setelah_perbarui = koleksi.jumlah()

    koleksi.hapus(["keu-02"])
    setelah_hapus = koleksi.jumlah()

    koleksi.tambah(
        ids=["keu-02"],
        teks=[record[indeks["keu-02"]]["teks"]],
        vektor=[record[indeks["keu-02"]]["vektor"]],
        metadata=[record[indeks["keu-02"]]["metadata"]],
    )
    setelah_pulih = koleksi.jumlah()

    demo_crud = {
        "jumlah_awal": sebelum,
        "setelah_perbarui": setelah_perbarui,
        "setelah_hapus": setelah_hapus,
        "setelah_pulih": setelah_pulih,
    }
    print(f"\nCRUD: {demo_crud}")

    statistik = vektor_db.statistik_koleksi(record)

    return {
        "model": model,
        "dimensi": dimensi,
        "jumlah_dokumen": len(record),
        "waktu_embedding_s": round(waktu_embedding, 2),
        "waktu_indexing_s": round(waktu_indexing, 2),
        "latensi_naive_rata_ms": round(total_naive / len(QUERY) * 1000, 3),
        "latensi_chroma_rata_ms": round(total_chroma / len(QUERY) * 1000, 3),
        "statistik": statistik,
        "hasil_query": hasil_query,
        "demo_filter": demo_filter,
        "demo_crud": demo_crud,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=MODEL_DEFAULT)
    parser.add_argument("--k", type=int, default=K_DEFAULT)
    parser.add_argument(
        "--path",
        type=Path,
        default=Path(__file__).parent / ".chroma",
        help="folder tempat Chroma menyimpan data",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "hasil_vectordb.json",
    )
    args = parser.parse_args()

    if args.k <= 0:
        raise SystemExit("--k harus > 0")

    hasil = jalankan(args.model, args.k, args.path)
    args.output.write_text(
        json.dumps(hasil, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nHasil mentah: {args.output}")


if __name__ == "__main__":
    main()
