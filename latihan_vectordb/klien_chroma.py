"""Klien Chroma untuk lab vector database.

Chroma berjalan lokal (PersistentClient) dan menyimpan datanya di folder
``.chroma``. Vektor dihitung sendiri lewat Ollama lalu dikirim apa adanya,
sehingga Chroma tidak perlu model embedding sendiri dan tidak butuh koneksi
internet.

Catatan penting: Chroma hanya menerima metadata bertipe str, int, float, atau
bool. List harus diubah menjadi string lebih dulu — itu tugas fungsi
``normalisasi_metadata()`` di ``vektor_db.py``.
"""

from pathlib import Path

import chromadb
from chromadb.config import Settings

PATH_DEFAULT = Path(__file__).parent / ".chroma"
NAMA_DEFAULT = "dokumen"


class KoleksiChroma:
    """Pembungkus tipis untuk Chroma agar dipakai di lab."""

    def __init__(
        self,
        path: str | Path = PATH_DEFAULT,
        nama: str = NAMA_DEFAULT,
        space: str = "cosine",
    ) -> None:
        self.path = Path(path)
        self.nama = nama
        self.space = space
        self.client = chromadb.PersistentClient(
            path=str(self.path),
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )
        self.koleksi = self._buka_koleksi()

    def _buka_koleksi(self):
        return self.client.get_or_create_collection(
            name=self.nama,
            metadata={"hnsw:space": self.space},
        )

    def reset(self) -> None:
        """Hapus koleksi lama, lalu buat baru dengan setting yang sama."""
        try:
            self.client.delete_collection(self.nama)
        except Exception:  # koleksi belum pernah dibuat
            pass
        self.koleksi = self._buka_koleksi()

    def tambah(
        self,
        ids: list[str],
        teks: list[str],
        vektor: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """Tambahkan dokumen baru. ID harus unik."""
        self.koleksi.add(
            ids=ids,
            documents=teks,
            embeddings=vektor,
            metadatas=metadata,
        )

    def perbarui(
        self,
        ids: list[str],
        teks: list[str],
        vektor: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """Upsert: tambah dokumen baru atau timpa dokumen dengan ID sama."""
        self.koleksi.upsert(
            ids=ids,
            documents=teks,
            embeddings=vektor,
            metadatas=metadata,
        )

    def hapus(self, ids: list[str]) -> None:
        """Hapus dokumen berdasarkan ID."""
        self.koleksi.delete(ids=ids)

    def cari(
        self,
        query_vec: list[float],
        k: int = 5,
        where: dict | None = None,
    ) -> list[dict]:
        """Cari dokumen terdekat dengan filter metadata opsional.

        Catatan: pada ``hnsw:space="cosine"``, Chroma mengembalikan *jarak*
        dengan nilai ``1 - cosine_similarity``. Skor similarity dikirim
        sebagai ``skor``.
        """
        parameter = {
            "query_embeddings": [query_vec],
            "n_results": max(1, min(k, self.jumlah())),
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            parameter["where"] = where

        hasil = self.koleksi.query(**parameter)

        daftar = []
        for nomor, id_dokumen in enumerate(hasil["ids"][0]):
            daftar.append(
                {
                    "id": id_dokumen,
                    "teks": hasil["documents"][0][nomor],
                    "metadata": hasil["metadatas"][0][nomor] or {},
                    "skor": round(1 - hasil["distances"][0][nomor], 6),
                    "jarak": round(hasil["distances"][0][nomor], 6),
                }
            )

        return daftar

    def jumlah(self) -> int:
        """Jumlah dokumen dalam koleksi."""
        return self.koleksi.count()

    def daftar_id(self) -> list[str]:
        """Semua ID yang tersimpan dalam koleksi."""
        return self.koleksi.get(include=[])["ids"]
