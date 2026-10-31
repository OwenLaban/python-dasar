"""Benchmark 3 model lokal Ollama pada tugas ekstraksi tiket.

Jalankan dari folder python-dasar:

    python -m latihan_lokal.benchmark_ollama

Semua model menerima prompt yang sama. Script mengukur latency, memvalidasi
JSON, dan menyimpan hasil mentah ke hasil_benchmark.json.
"""

import argparse
import json
import time
from pathlib import Path

import requests

OLLAMA_API = "http://localhost:11434"
MODELS_DEFAULT = ["llama3.2:1b", "qwen2.5:1.5b", "gemma2:2b"]
FIELD_WAJIB = ["nama", "email", "topik", "sentimen", "butuh_eskalasi"]

EMAIL = """Halo tim support,

Saya Rina dari PT Sinar Jaya. Pesanan #4821 yang saya bayar minggu lalu
belum sampai, padahal kurir bilang paket sudah dikirim. Saya sudah coba
chat tapi tidak ada balasan. Tolong dicek ya, ini sudah terlambat untuk
acara kami hari Jumat.

Email: rina@sinarjaya.co.id"""

PROMPT = f"""Ekstrak informasi dari email pelanggan berikut.

Balas HANYA dengan JSON valid, tanpa markdown, dengan schema:
{{
  "nama": string atau null,
  "email": string atau null,
  "topik": ringkasan singkat,
  "sentimen": "positif" | "netral" | "negatif",
  "butuh_eskalasi": true atau false
}}

Email:
{EMAIL}"""


def cek_ollama(url: str = OLLAMA_API) -> list[str]:
    """Kembalikan daftar nama model yang terpasang di Ollama."""
    response = requests.get(f"{url}/api/tags", timeout=5)
    response.raise_for_status()
    return [model["name"] for model in response.json().get("models", [])]


def _field_lengkap(data: object) -> bool:
    return isinstance(data, dict) and all(field in data for field in FIELD_WAJIB)


def jalankan_model(
    model: str,
    prompt: str = PROMPT,
    url: str = OLLAMA_API,
) -> dict:
    """Jalankan satu model dan kembalikan hasil terukur."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 200,
            "num_ctx": 2048,
        },
    }

    mulai = time.perf_counter()
    response = requests.post(f"{url}/api/generate", json=payload, timeout=300)
    response.raise_for_status()
    detik = time.perf_counter() - mulai

    body = response.json()
    teks = body.get("response", "")
    try:
        data = json.loads(teks)
        valid = True
    except json.JSONDecodeError:
        data = None
        valid = False

    eval_count = body.get("eval_count", 0)
    eval_duration = body.get("eval_duration", 0)
    token_per_detik = (
        round(eval_count / (eval_duration / 1_000_000_000), 2)
        if eval_count and eval_duration
        else None
    )

    return {
        "model": model,
        "latency_s": round(detik, 2),
        "token_per_detik": token_per_detik,
        "valid_json": valid,
        "field_lengkap": _field_lengkap(data),
        "output": data,
        "raw": teks,
    }


def benchmark(models: list[str], prompt: str = PROMPT, url: str = OLLAMA_API) -> list[dict]:
    """Jalankan semua model; error satu model tidak menghentikan yang lain."""
    hasil = []
    for model in models:
        print(f"Menjalankan {model} ...", flush=True)
        try:
            hasil.append(jalankan_model(model, prompt=prompt, url=url))
        except requests.RequestException as error:
            hasil.append({"model": model, "error": str(error)})
    return hasil


def simpan_hasil(hasil: list[dict], path: Path) -> None:
    path.write_text(json.dumps(hasil, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark model lokal Ollama")
    parser.add_argument(
        "--models",
        nargs="+",
        default=MODELS_DEFAULT,
        help="Daftar model Ollama (default: 3 model kecil)",
    )
    args = parser.parse_args()

    try:
        tersedia = cek_ollama()
    except requests.RequestException:
        print("Ollama tidak berjalan. Jalankan `ollama serve` atau buka aplikasinya.")
        return

    print(f"Model terpasang: {', '.join(tersedia) if tersedia else '(kosong)'}")
    dipakai = [model for model in args.models if model in tersedia]
    hilang = [model for model in args.models if model not in tersedia]

    if hilang:
        print(f"Belum di-pull: {', '.join(hilang)}")
        print("Jalankan: " + " ; ".join(f"ollama pull {model}" for model in hilang))

    if not dipakai:
        print("Tidak ada model yang bisa dijalankan.")
        return

    hasil = benchmark(dipakai)
    print()
    print(f"{'MODEL':<20} {'LATENCY':>9} {'TOK/S':>7} {'JSON':>6} {'FIELD':>6}")
    print("-" * 54)
    for item in hasil:
        if "error" in item:
            print(f"{item['model']:<20} ERROR: {item['error']}")
            continue
        tok = f"{item['token_per_detik']:.1f}" if item["token_per_detik"] else "-"
        print(
            f"{item['model']:<20} {item['latency_s']:>8.2f}s {tok:>7} "
            f"{'ya' if item['valid_json'] else 'tidak':>6} "
            f"{'ya' if item['field_lengkap'] else 'tidak':>6}"
        )

    path = Path(__file__).with_name("hasil_benchmark.json")
    simpan_hasil(hasil, path)
    print(f"\nHasil mentah disimpan ke {path}")


if __name__ == "__main__":
    main()
