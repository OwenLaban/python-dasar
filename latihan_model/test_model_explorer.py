"""Test lab ekosistem model. Tidak memanggil jaringan."""

from latihan_model import model_explorer

MODELS = [
    {
        "id": "sedang",
        "name": "Model Sedang",
        "context_length": 200_000,
        "pricing": {"prompt": "0.000003", "completion": "0.000015"},
        "architecture": {"input_modalities": ["text"]},
        "supported_parameters": ["response_format", "tools"],
    },
    {
        "id": "mahal",
        "name": "Model Mahal",
        "context_length": 1_000_000,
        "pricing": {"prompt": "0.00003", "completion": "0.00006"},
        "architecture": {"input_modalities": ["text", "image"]},
        "supported_parameters": ["response_format"],
    },
    {
        "id": "murah",
        "name": "Model Murah",
        "context_length": 128_000,
        "pricing": {"prompt": "0", "completion": "0"},
        "architecture": {"input_modalities": ["text"]},
        "supported_parameters": ["response_format"],
    },
    {
        "id": "kecil",
        "name": "Model Kecil",
        "context_length": 8_000,
        "pricing": {"prompt": "0.000001", "completion": "0.000002"},
        "architecture": {"input_modalities": ["text"]},
        "supported_parameters": [],
    },
]


class FakeResponse:
    def __init__(self, data: dict):
        self._data = data
        self.raise_for_status_dipanggil = False

    def raise_for_status(self):
        self.raise_for_status_dipanggil = True

    def json(self):
        return self._data


def test_ambil_model(monkeypatch):
    response = FakeResponse({"data": MODELS})

    def fake_get(url, timeout):
        assert url == model_explorer.MODELS_URL
        assert timeout == 30
        return response

    monkeypatch.setattr(model_explorer.requests, "get", fake_get)

    hasil = model_explorer.ambil_model()

    assert hasil == MODELS
    assert response.raise_for_status_dipanggil is True


def test_harga_per_juta():
    assert model_explorer.harga_per_juta(MODELS[0]) == (3.0, 15.0)


def test_filter_model():
    hasil = model_explorer.filter_model(
        MODELS,
        maks_prompt_per_juta=10,
        min_context=32_000,
        butuh_json=True,
    )

    assert [m["id"] for m in hasil] == ["sedang", "murah"]


def test_filter_model_gratis_saja():
    hasil = model_explorer.filter_model(
        MODELS,
        maks_prompt_per_juta=100,
        gratis_saja=True,
    )

    assert [m["id"] for m in hasil] == ["murah"]


def test_filter_model_min_context():
    hasil = model_explorer.filter_model(
        MODELS,
        maks_prompt_per_juta=100,
        min_context=100_000,
    )

    assert [m["id"] for m in hasil] == ["sedang", "mahal", "murah"]


def test_urutkan_termurah():
    hasil = model_explorer.urutkan_termurah(MODELS)

    assert [m["id"] for m in hasil] == ["murah", "kecil", "sedang", "mahal"]
    assert MODELS[0]["id"] == "sedang"


def test_ringkas_model():
    assert model_explorer.ringkas_model(MODELS[0]) == {
        "id": "sedang",
        "nama": "Model Sedang",
        "context": 200_000,
        "prompt_per_juta": 3.0,
        "completion_per_juta": 15.0,
        "modalitas": ["text"],
        "dukung_json": True,
    }
