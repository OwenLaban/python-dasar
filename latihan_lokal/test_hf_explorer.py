"""Test lab Hugging Face. Tidak memanggil jaringan."""

import pytest

from latihan_lokal import hf_explorer

MODELS = [
    {
        "id": "org/kecil",
        "downloads": 1_000,
        "likes": 10,
        "pipeline_tag": "text-generation",
        "library_name": "transformers",
        "tags": ["license:apache-2.0", "text-generation"],
        "gated": False,
        "safetensors": {"total": 1_000_000_000},
    },
    {
        "id": "org/kecil2",
        "downloads": 5_000,
        "likes": 50,
        "pipeline_tag": "text-generation",
        "library_name": "transformers",
        "tags": ["license:mit", "text-generation"],
        "gated": False,
        "safetensors": {"total": 2_000_000_000},
    },
    {
        "id": "org/sedang",
        "downloads": 9_000,
        "likes": 90,
        "pipeline_tag": "text-generation",
        "library_name": "transformers",
        "tags": ["license:apache-2.0"],
        "gated": False,
        "safetensors": {"total": 7_000_000_000},
    },
    {
        "id": "org/embedding",
        "downloads": 20_000,
        "likes": 200,
        "pipeline_tag": "feature-extraction",
        "library_name": "sentence-transformers",
        "tags": ["license:apache-2.0"],
        "gated": False,
        "safetensors": {"total": 100_000_000},
    },
    {
        "id": "org/gated",
        "downloads": 30_000,
        "likes": 300,
        "pipeline_tag": "text-generation",
        "library_name": "transformers",
        "tags": ["license:cc-by-nc-4.0"],
        "gated": "manual",
        "safetensors": {"total": 1_000_000_000},
    },
    {
        "id": "org/tanpa-ukuran",
        "downloads": 40_000,
        "likes": 400,
        "pipeline_tag": "text-generation",
        "library_name": "transformers",
        "tags": [],
        "gated": False,
    },
]

DETAIL = {
    "id": "org/kecil2",
    "downloads": 5_000,
    "likes": 50,
    "pipeline_tag": "text-generation",
    "library_name": "transformers",
    "tags": ["license:mit", "text-generation"],
    "gated": False,
    "safetensors": {"total": 2_000_000_000},
}


class FakeResponse:
    def __init__(self, data):
        self._data = data
        self.raise_for_status_dipanggil = False

    def raise_for_status(self):
        self.raise_for_status_dipanggil = True

    def json(self):
        return self._data


def test_ambil_model_hf(monkeypatch):
    response = FakeResponse(MODELS)
    dipanggil = {}

    def fake_get(url, params, timeout):
        dipanggil["url"] = url
        dipanggil["params"] = params
        dipanggil["timeout"] = timeout
        return response

    monkeypatch.setattr(hf_explorer.requests, "get", fake_get)

    hasil = hf_explorer.ambil_model_hf("qwen", limit=5)

    assert hasil == MODELS
    assert response.raise_for_status_dipanggil is True
    assert dipanggil["url"] == hf_explorer.HF_API
    assert dipanggil["params"] == {
        "search": "qwen",
        "limit": 5,
        "sort": "downloads",
        "direction": -1,
    }
    assert dipanggil["timeout"] == 30


def test_ambil_model_hf_dengan_task(monkeypatch):
    response = FakeResponse(MODELS)
    dipanggil = {}

    def fake_get(url, params, timeout):
        dipanggil["params"] = params
        return response

    monkeypatch.setattr(hf_explorer.requests, "get", fake_get)

    hf_explorer.ambil_model_hf("qwen", task="text-generation", limit=3)

    assert dipanggil["params"]["filter"] == "text-generation"
    assert dipanggil["params"]["limit"] == 3


def test_ambil_detail_hf(monkeypatch):
    response = FakeResponse(DETAIL)
    dipanggil = {}

    def fake_get(url, timeout):
        dipanggil["url"] = url
        dipanggil["timeout"] = timeout
        return response

    monkeypatch.setattr(hf_explorer.requests, "get", fake_get)

    hasil = hf_explorer.ambil_detail_hf("org/kecil2")

    assert hasil == DETAIL
    assert dipanggil["url"] == f"{hf_explorer.HF_API}/org/kecil2"
    assert dipanggil["timeout"] == 30
    assert response.raise_for_status_dipanggil is True


def test_estimasi_q4_gb():
    assert hf_explorer.estimasi_q4_gb(MODELS[1]) == pytest.approx(1.1)


def test_estimasi_q4_gb_tanpa_data():
    assert hf_explorer.estimasi_q4_gb(MODELS[5]) is None


def test_ringkas_model_hf():
    assert hf_explorer.ringkas_model_hf(MODELS[1]) == {
        "id": "org/kecil2",
        "downloads": 5_000,
        "likes": 50,
        "task": "text-generation",
        "library": "transformers",
        "license": "mit",
        "gated": False,
        "params": 2_000_000_000,
        "q4_gb": pytest.approx(1.1),
    }


def test_ringkas_model_tanpa_license_dan_ukuran():
    hasil = hf_explorer.ringkas_model_hf(MODELS[5])

    assert hasil["license"] is None
    assert hasil["params"] is None
    assert hasil["q4_gb"] is None


def test_pilih_model_lokal():
    hasil = hf_explorer.pilih_model_lokal(MODELS, max_vram_gb=2.0)

    assert [m["id"] for m in hasil] == ["org/kecil2", "org/kecil"]


def test_pilih_model_lokal_vram_besar():
    hasil = hf_explorer.pilih_model_lokal(MODELS, max_vram_gb=8.0)

    assert [m["id"] for m in hasil] == [
        "org/sedang",
        "org/kecil2",
        "org/kecil",
    ]
