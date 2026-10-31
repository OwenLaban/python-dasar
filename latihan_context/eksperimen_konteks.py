"""Eksperimen kecil: apakah posisi informasi memengaruhi jawaban model?

Konsep yang diuji: **lost in the middle**. Informasi yang sama diletakkan di
awal, tengah, dan akhir dokumen. Model diminta mengambil satu kode rahasia.

Jalankan setelah fungsi di ``konteks.py`` selesai:

    python -m latihan_context.eksperimen_konteks

Hasil mentah disimpan ke ``hasil_konteks.json``.
"""

import argparse
import json
import time
from pathlib import Path

import requests

from latihan_context.konteks import hitung_token

OLLAMA_API = "http://localhost:11434"
MODEL_DEFAULT = "qwen2.5:1.5b"
NEEDLE = "BIRU-4721"
POSISI = ("awal", "tengah", "akhir")

PROMPT = """Dokumen berikut berisi catatan operasional. Di dalamnya ada satu kode rahasia berbentuk KATA-ANGKA.

DOKUMEN:
{dokumen}

Pertanyaan: Apa kode rahasia yang tertulis di dokumen? Balas hanya kodenya."""


def susun_dokumen(posisi: str, jumlah_baris: int = 60) -> str:
    """Susun dokumen dengan kode rahasia di posisi tertentu."""
    if posisi not in POSISI:
        raise ValueError(f"posisi harus salah satu dari {POSISI}")
    if jumlah_baris < 1:
        raise ValueError("jumlah_baris harus > 0")

    baris = [
        (
            f"Catatan operasional nomor {i}: tim gudang memeriksa stok, "
            "jadwal pengiriman, dan laporan harian."
        )
        for i in range(jumlah_baris)
    ]
    kode = f"Kode rahasia yang harus diingat: {NEEDLE}."

    if posisi == "awal":
        indeks = 0
    elif posisi == "tengah":
        indeks = len(baris) // 2
    else:
        indeks = len(baris)

    baris.insert(indeks, kode)
    return "\n".join(baris)


def jalankan_posisi(
    posisi: str,
    model: str = MODEL_DEFAULT,
    jumlah_baris: int = 60,
    url: str = OLLAMA_API,
) -> dict:
    """Jalankan satu percobaan dan kembalikan hasil terukur."""
    dokumen = susun_dokumen(posisi, jumlah_baris)
    prompt = PROMPT.format(dokumen=dokumen)
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 20,
            "num_ctx": 2048,
        },
    }

    mulai = time.perf_counter()
    response = requests.post(f"{url}/api/generate", json=payload, timeout=300)
    response.raise_for_status()
    latency = time.perf_counter() - mulai

    body = response.json()
    jawaban = body.get("response", "").strip()
    return {
        "posisi": posisi,
        "token_dokumen": hitung_token(dokumen),
        "token_prompt": hitung_token(prompt),
        "jawaban": jawaban,
        "benar": NEEDLE.lower() in jawaban.lower(),
        "latency_s": round(latency, 2),
    }


def cek_model(model: str, url: str = OLLAMA_API) -> list[str]:
    """Kembalikan daftar model Ollama yang terpasang."""
    response = requests.get(f"{url}/api/tags", timeout=5)
    response.raise_for_status()
    return [item["name"] for item in response.json().get("models", [])]


def simpan_hasil(hasil: list[dict], path: Path) -> None:
    path.write_text(json.dumps(hasil, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Eksperimen posisi informasi")
    parser.add_argument("--model", default=MODEL_DEFAULT)
    parser.add_argument("--baris", type=int, default=60)
    args = parser.parse_args()

    try:
        tersedia = cek_model(args.model)
    except requests.RequestException as error:
        print(f"Ollama tidak bisa dihubungi: {error}")
        return

    if args.model not in tersedia:
        print(f"Model {args.model} belum terpasang.")
        print(f"Jalankan: ollama pull {args.model}")
        return

    hasil = []
    print(f"Model: {args.model}")
    print(f"Kode rahasia: {NEEDLE}")
    print(f"Jumlah baris filler: {args.baris}\n")

    for posisi in POSISI:
        print(f"Menjalankan posisi {posisi} ...", flush=True)
        try:
            item = jalankan_posisi(
                posisi,
                model=args.model,
                jumlah_baris=args.baris,
            )
        except requests.RequestException as error:
            item = {"posisi": posisi, "error": str(error)}
        hasil.append(item)

    print()
    print(f"{'POSISI':<10} {'TOKEN':>6} {'LATENCY':>9} {'BENAR':>6}  JAWABAN")
    print("-" * 72)
    for item in hasil:
        if "error" in item:
            print(f"{item['posisi']:<10} ERROR: {item['error']}")
            continue
        jawaban = item["jawaban"].replace("\n", " ")[:35]
        print(
            f"{item['posisi']:<10} {item['token_dokumen']:>6} "
            f"{item['latency_s']:>8.2f}s {'ya' if item['benar'] else 'tidak':>6}  "
            f"{jawaban}"
        )

    path = Path(__file__).with_name("hasil_konteks.json")
    simpan_hasil(hasil, path)
    print(f"\nHasil mentah disimpan ke {path}")


if __name__ == "__main__":
    main()
