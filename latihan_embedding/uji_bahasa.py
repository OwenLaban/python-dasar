"""Uji tambahan: pengaruh bahasa query terhadap hasil retrieval.

Jalankan setelah ``vektor.py`` lulus test:

    .\\.venv\\Scripts\\python.exe -m latihan_embedding.uji_bahasa

Semua query diuji terhadap 20 kalimat yang sama, dengan topik target
``keuangan``.
"""

from latihan_embedding import vektor
from latihan_embedding.kalimat import KALIMAT
from latihan_embedding.klien_embedding import EmbeddingClient, EmbeddingError

QUERY = {
    "id": "cara mengelola uang agar tidak cepat habis",
    "en": "how to manage money so it does not run out quickly",
    "id_pendek": "mengelola uang",
    "en_pendek": "manage money",
}

TOPIK_TARGET = "keuangan"


def main() -> None:
    client = EmbeddingClient()

    try:
        vektor_kalimat = client.embed([item["teks"] for item in KALIMAT])
        vektor_query = client.embed(list(QUERY.values()))
    except EmbeddingError as error:
        raise SystemExit(f"Error: {error}") from error

    kandidat = [
        {**item, "vektor": vektor.normalisasi(vec)}
        for item, vec in zip(KALIMAT, vektor_kalimat)
    ]

    print(f"Model: {client.model}")
    print(f"Kalimat: {len(KALIMAT)}")
    print(f"Topik target: {TOPIK_TARGET}")

    for label, teks in zip(QUERY, vektor_query):
        query_vec = vektor.normalisasi(teks)
        teratas = vektor.cari_terdekat(query_vec, kandidat, k=3)
        precision = vektor.precision_at_k(teratas, TOPIK_TARGET, k=3)

        print(f"\n[{label}] {QUERY[label]}")
        for nomor, hasil in enumerate(teratas, start=1):
            print(
                f"  {nomor}. [{hasil['skor']:.4f}] ({hasil['topik']}) "
                f"{hasil['teks']}"
            )
        print(f"  precision@3 ({TOPIK_TARGET}): {precision:.2f}")


if __name__ == "__main__":
    main()
