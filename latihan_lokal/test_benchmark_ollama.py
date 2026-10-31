"""Test benchmark Ollama. Tidak memanggil jaringan."""

from latihan_lokal import benchmark_ollama


class FakeResponse:
    def __init__(self, data):
        self._data = data
        self.raise_for_status_dipanggil = False

    def raise_for_status(self):
        self.raise_for_status_dipanggil = True

    def json(self):
        return self._data


def test_cek_ollama(monkeypatch):
    response = FakeResponse({"models": [{"name": "llama3.2:1b"}, {"name": "qwen2.5:1.5b"}]})

    def fake_get(url, timeout):
        assert url == f"{benchmark_ollama.OLLAMA_API}/api/tags"
        assert timeout == 5
        return response

    monkeypatch.setattr(benchmark_ollama.requests, "get", fake_get)

    assert benchmark_ollama.cek_ollama() == ["llama3.2:1b", "qwen2.5:1.5b"]
    assert response.raise_for_status_dipanggil is True


def test_jalankan_model_json_valid(monkeypatch):
    output = {
        "nama": "Rina",
        "email": "rina@sinarjaya.co.id",
        "topik": "pesanan belum sampai",
        "sentimen": "negatif",
        "butuh_eskalasi": True,
    }
    response = FakeResponse(
        {
            "response": __import__("json").dumps(output),
            "eval_count": 50,
            "eval_duration": 2_000_000_000,
        }
    )
    payload_dikirim = {}

    def fake_post(url, json, timeout):
        payload_dikirim.update(json)
        assert url == f"{benchmark_ollama.OLLAMA_API}/api/generate"
        assert timeout == 300
        return response

    monkeypatch.setattr(benchmark_ollama.requests, "post", fake_post)

    hasil = benchmark_ollama.jalankan_model("llama3.2:1b")

    assert payload_dikirim["model"] == "llama3.2:1b"
    assert payload_dikirim["format"] == "json"
    assert payload_dikirim["stream"] is False
    assert payload_dikirim["options"]["temperature"] == 0
    assert hasil["valid_json"] is True
    assert hasil["field_lengkap"] is True
    assert hasil["output"] == output
    assert hasil["token_per_detik"] == 25.0


def test_jalankan_model_json_rusak(monkeypatch):
    response = FakeResponse({"response": "ini bukan JSON"})

    def fake_post(url, json, timeout):
        return response

    monkeypatch.setattr(benchmark_ollama.requests, "post", fake_post)

    hasil = benchmark_ollama.jalankan_model("gemma2:2b")

    assert hasil["valid_json"] is False
    assert hasil["field_lengkap"] is False
    assert hasil["output"] is None
