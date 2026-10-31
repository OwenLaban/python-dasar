"""Lab Minggu 11 — menjelajahi Hugging Face Hub.

Jalankan dari folder python-dasar:

    python -m latihan_lokal.hf_explorer

Endpoint metadata publik tidak butuh token.
"""

import requests

HF_API = "https://huggingface.co/api/models"


def ambil_model_hf(
    search: str,
    task: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Ambil daftar model publik dari Hugging Face Hub.

    Parameter query:
    - search: kata kunci nama model
    - limit: jumlah maksimal hasil
    - sort: "downloads"
    - direction: -1 (paling banyak diunduh dulu)
    - filter: task, hanya jika task tidak None

    TODO:
    1. Susun dict params.
    2. response = requests.get(HF_API, params=params, timeout=30)
    3. response.raise_for_status()
    4. return response.json()
    """
    raise NotImplementedError("TODO: implementasikan ambil_model_hf()")


def ambil_detail_hf(model_id: str) -> dict:
    """Ambil detail satu model, termasuk jumlah parameter di `safetensors.total`.

    Endpoint: GET https://huggingface.co/api/models/{model_id}

    TODO:
    1. response = requests.get(f"{HF_API}/{model_id}", timeout=30)
    2. response.raise_for_status()
    3. return response.json()
    """
    raise NotImplementedError("TODO: implementasikan ambil_detail_hf()")


def estimasi_q4_gb(model: dict) -> float | None:
    """Perkiraan ukuran bobot Q4_K_M dalam GB.

    Q4_K_M memakai sekitar 4,5 bit per parameter, ditambah overhead.
    Perkiraan kasar: total_parameter × 0,55 byte / 1_000_000_000.

    Jika `safetensors.total` tidak ada, kembalikan None.
    Endpoint list HF sering tidak menyertakan field ini; ambil detail model
    dulu dengan `ambil_detail_hf()`.

    TODO:
    1. total = model.get("safetensors", {}).get("total")
    2. jika tidak ada, return None
    3. return round(total * 0.55 / 1_000_000_000, 2)
    """
    raise NotImplementedError("TODO: implementasikan estimasi_q4_gb()")


def ringkas_model_hf(model: dict) -> dict:
    """Buat ringkasan metadata satu model.

    Bentuk hasil:
    {
        "id": model["id"],
        "downloads": model.get("downloads", 0),
        "likes": model.get("likes", 0),
        "task": model.get("pipeline_tag"),
        "library": model.get("library_name"),
        "license": nama license dari tag "license:..." atau None,
        "gated": bool(model.get("gated", False)),
        "params": model.get("safetensors", {}).get("total"),
        "q4_gb": estimasi_q4_gb(model),
    }

    TODO: implementasikan.
    """
    raise NotImplementedError("TODO: implementasikan ringkas_model_hf()")


def pilih_model_lokal(
    models: list[dict],
    max_vram_gb: float = 2.0,
    margin: float = 0.85,
) -> list[dict]:
    """Pilih model yang realistis berjalan di VRAM terbatas.

    Aturan:
    - hanya `pipeline_tag == "text-generation"`;
    - lewati model `gated` (butuh login/izin);
    - estimasi Q4 harus ada dan <= max_vram_gb × margin;
    - urutkan dari downloads terbanyak.

    TODO: implementasikan.
    """
    raise NotImplementedError("TODO: implementasikan pilih_model_lokal()")


def main() -> None:
    print("Mencari model text-generation 'instruct' di Hugging Face...")
    models = ambil_model_hf("instruct", task="text-generation", limit=8)
    print(f"Ditemukan: {len(models)} model\n")

    print(f"{'MODEL':<52} {'DOWNLOADS':>12} {'Q4 (GB)':>8}")
    print("-" * 76)
    for model in models[:6]:
        detail = ambil_detail_hf(model["id"])
        detail.setdefault("downloads", model.get("downloads", 0))
        detail.setdefault("likes", model.get("likes", 0))
        detail.setdefault("pipeline_tag", model.get("pipeline_tag"))
        detail.setdefault("library_name", model.get("library_name"))
        detail.setdefault("tags", model.get("tags", []))
        r = ringkas_model_hf(detail)
        q4 = f"{r['q4_gb']:.2f}" if r["q4_gb"] is not None else "?"
        print(f"{r['id']:<52} {r['downloads']:>12,} {q4:>8}")


if __name__ == "__main__":
    main()
