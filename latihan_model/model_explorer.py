"""Lab Minggu 10 — menjelajahi katalog model OpenRouter.

Jalankan dari folder python-dasar:

    python -m latihan_model.model_explorer

Endpoint /models gratis dan tidak butuh API key.
"""

import requests

MODELS_URL = "https://openrouter.ai/api/v1/models"


def ambil_model(url: str = MODELS_URL) -> list[dict]:
    """Ambil daftar model dari OpenRouter.

    TODO:
    1. response = requests.get(url, timeout=30)
    2. response.raise_for_status()
    3. return response.json()["data"]
    """
    raise NotImplementedError("TODO: implementasikan ambil_model()")


def harga_per_juta(model: dict) -> tuple[float, float]:
    """Kembalikan (harga prompt, harga completion) dalam USD per 1 juta token.

    OpenRouter menyimpan harga per token sebagai string, misalnya "0.000003".
    Kalikan dengan 1_000_000 untuk mendapat harga per juta token.

    TODO:
    1. prompt = float(model["pricing"]["prompt"]) * 1_000_000
    2. completion = float(model["pricing"]["completion"]) * 1_000_000
    3. return prompt, completion
    """
    raise NotImplementedError("TODO: implementasikan harga_per_juta()")


def filter_model(
    models: list[dict],
    maks_prompt_per_juta: float,
    min_context: int = 0,
    gratis_saja: bool = False,
    butuh_json: bool = False,
) -> list[dict]:
    """Saring model sesuai kebutuhan.

    Aturan:
    - context_length >= min_context
    - harga prompt <= maks_prompt_per_juta
    - jika gratis_saja: harga prompt DAN completion harus 0
    - jika butuh_json: "response_format" harus ada di supported_parameters
    - abaikan model dengan harga negatif (harganya variabel/tidak pasti)

    TODO: loop models, hitung harga dengan harga_per_juta(), cek semua aturan,
    lalu kumpulkan model yang lolos. Pertahankan urutan asli.
    """
    raise NotImplementedError("TODO: implementasikan filter_model()")


def urutkan_termurah(models: list[dict]) -> list[dict]:
    """Urutkan dari harga prompt termurah, lalu completion termurah.

    TODO: gunakan sorted() dengan key (prompt, completion).
    Jangan mengubah list asli.
    """
    raise NotImplementedError("TODO: implementasikan urutkan_termurah()")


def ringkas_model(model: dict) -> dict:
    """Buat ringkasan satu model untuk ditampilkan.

    TODO: kembalikan dict dengan bentuk:
    {
        "id": model["id"],
        "nama": model["name"],
        "context": model["context_length"],
        "prompt_per_juta": round(prompt, 4),
        "completion_per_juta": round(completion, 4),
        "modalitas": model.get("architecture", {}).get("input_modalities", []),
        "dukung_json": "response_format" in model.get("supported_parameters", []),
    }
    """
    raise NotImplementedError("TODO: implementasikan ringkas_model()")


def main() -> None:
    models = ambil_model()
    print(f"Total model di OpenRouter: {len(models)}")

    kandidat = filter_model(
        models,
        maks_prompt_per_juta=1.0,
        min_context=32_000,
        butuh_json=True,
    )
    kandidat = urutkan_termurah(kandidat)

    print(f"Kandidat <= $1/M prompt, >= 32k context, dukung JSON: {len(kandidat)}")
    print()
    print(f"{'MODEL':<48} {'PROMPT/M':>9} {'COMPL/M':>9} {'CONTEXT':>9}")
    print("-" * 80)
    for model in kandidat[:15]:
        r = ringkas_model(model)
        print(
            f"{r['id']:<48} {r['prompt_per_juta']:>9.2f} "
            f"{r['completion_per_juta']:>9.2f} {r['context']:>9,}"
        )


if __name__ == "__main__":
    main()
