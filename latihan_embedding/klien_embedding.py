"""Klien embedding lokal lewat Ollama.

Model default: ``nomic-embed-text`` (768 dimensi, sekitar 274 MB).
Tidak perlu API key dan tidak perlu install PyTorch.
"""

from dataclasses import dataclass

import requests

OLLAMA_URL = "http://localhost:11434"
MODEL_DEFAULT = "nomic-embed-text"


class EmbeddingError(RuntimeError):
    """Ollama tidak bisa dihubungi atau mengembalikan embedding tidak valid."""


@dataclass
class EmbeddingClient:
    base_url: str = OLLAMA_URL
    model: str = MODEL_DEFAULT
    timeout: int = 120

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")

    def daftar_model(self) -> list[str]:
        """Kembalikan nama model yang terpasang di Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
        except requests.RequestException as error:
            raise EmbeddingError(
                f"Tidak bisa menghubungi Ollama di {self.base_url}. "
                "Jalankan `ollama serve` terlebih dahulu."
            ) from error

        body = response.json()
        return [model["name"] for model in body.get("models", [])]

    def embed(self, teks: str | list[str]) -> list[list[float]]:
        """Ubah satu teks atau beberapa teks menjadi vektor."""
        if isinstance(teks, str):
            if not teks.strip():
                raise ValueError("teks tidak boleh kosong")
            input_data: str | list[str] = teks
        else:
            if not teks or any(not item.strip() for item in teks):
                raise ValueError("daftar teks tidak boleh kosong")
            input_data = list(teks)

        payload = {"model": self.model, "input": input_data}

        try:
            response = requests.post(
                f"{self.base_url}/api/embed",
                json=payload,
                timeout=self.timeout,
            )
        except requests.Timeout as error:
            raise EmbeddingError(
                f"Ollama melewati batas waktu {self.timeout} detik."
            ) from error
        except requests.RequestException as error:
            raise EmbeddingError(
                f"Gagal menghubungi Ollama di {self.base_url}."
            ) from error

        if response.status_code >= 400:
            detail = response.text[:300]
            raise EmbeddingError(
                f"Ollama menolak permintaan (HTTP {response.status_code}): {detail}"
            )

        try:
            body = response.json()
        except ValueError as error:
            raise EmbeddingError("Respons Ollama bukan JSON.") from error

        embeddings = body.get("embeddings")
        if not embeddings:
            raise EmbeddingError("Ollama tidak mengembalikan embedding.")

        dimensi = len(embeddings[0])
        if dimensi == 0 or any(len(item) != dimensi for item in embeddings):
            raise EmbeddingError("Dimensi embedding tidak konsisten.")

        return embeddings

    def embed_satu(self, teks: str) -> list[float]:
        """Ubah satu teks menjadi satu vektor."""
        return self.embed(teks)[0]
