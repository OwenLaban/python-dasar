"""Eksperimen semantic search dengan embedding lokal.

Jalankan setelah semua fungsi di ``vektor.py`` lulus test:

    .\.venv\Scripts\python.exe -m latihan_embedding.eksperimen_embedding
"""

import argparse
import json
import time
from pathlib import Path

from latihan_embedding import vektor
from latihan_embedding.kalimat import KALIMAT, QUERY
from latihan_embedding.klien_embedding import (
    MODEL_DEFAULT,
    EmbeddingClient,
    EmbeddingError,
)


def jalankan(model: str, k: int = 3) -> dict:
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
    print(f"Kalimat: {len(KALIMAT)}")
    print("Membuat embedding ...", flush=True)

    mulai = time.perf_counter()
    try:
        vektor_kalimat = client.embed([item["teks"] for item in KALIMAT])
        vektor_query = client.embed([item["teks"] for item in QUERY])
    except EmbeddingError as error:
        raise SystemExit(f"Error: {error}") from error
    waktu_embed = time.perf_counter() - mulai

    kandidat = [
        {
            "teks": item["teks"],
            "topik": item["topik"],
            "vektor": vektor.normalisasi(vec),
        }
        for item, vec in zip(KALIMAT, vektor_kalimat)
    ]

    hasil_query = []
    for item, vec in zip(QUERY, vektor_query):
        query_vec = vektor.normalisasi(vec)
        teratas = vektor.cari_terdekat(query_vec, kandidat, k=k)
        precision = vektor.precision_at_k(teratas, item["topik"], k=k)
        hasil_query.append(
            {
                "query": item["teks"],
                "topik_target": item["topik"],
                "precision_at_k": round(precision, 4),
                "top_k": [
                    {
                        "teks": hasil["teks"],
                        "topik": hasil["topik"],
                        "skor": round(hasil["skor"], 4),
                    }
                    for hasil in teratas
                ],
            }
        )

        print(f"\nQuery: {item['teks']}")
        for nomor, hasil in enumerate(teratas, start=1):
            print(
                f"  {nomor}. [{hasil['skor']:.3f}] ({hasil['topik']}) "
                f"{hasil['teks']}"
            )
        print(f"  precision@{k}: {precision:.2f}")

    dimensi = len(vektor_kalimat[0])
    print(f"\nDimensi embedding: {dimensi}")
    print(f"Waktu embedding: {waktu_embed:.2f} s")

    return {
        "model": model,
        "dimensi": dimensi,
        "jumlah_kalimat": len(KALIMAT),
        "waktu_embed_s": round(waktu_embed, 2),
        "hasil": hasil_query,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=MODEL_DEFAULT)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "hasil_embedding.json",
    )
    args = parser.parse_args()

    if args.k <= 0:
        raise SystemExit("--k harus > 0")

    hasil = jalankan(args.model, k=args.k)
    args.output.write_text(
        json.dumps(hasil, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nHasil mentah: {args.output}")


if __name__ == "__main__":
    main()
