# Lab Minggu 10 — Ekosistem Model

**Status: ✅ Selesai** — 5 fungsi diimplementasikan, **7/7 test lulus**, dan
laporan pemilihan model untuk tiga skenario sudah terisi.

Tujuan: belajar **memilih model berdasarkan kebutuhan**, bukan berdasarkan
model yang paling ramai dibicarakan.

Lab ini memakai katalog publik OpenRouter (`/api/v1/models`) yang bisa diakses
**tanpa API key**. Kamu akan menyaring model berdasarkan harga, context window,
dan dukungan structured output, lalu menulis rekomendasi untuk tiga skenario.

## File

```text
latihan_model/
├── README.md            # instruksi dan hasil
├── studi_kasus.md       # 3 skenario nyata
├── model_explorer.py    # explorer katalog + filter model
├── test_model_explorer.py
└── laporan_model.md     # laporan pemilihan model (sudah terisi)
```

## Alur

1. Baca `studi_kasus.md`.
2. Implementasikan 5 fungsi di `model_explorer.py`.
3. Jalankan test sampai hijau:

   ```powershell
   .\.venv\Scripts\python.exe -m pytest latihan_model -v
   ```

4. Jalankan explorer untuk melihat kandidat nyata:

   ```powershell
   .\.venv\Scripts\python.exe -m latihan_model.model_explorer
   ```

5. Isi `laporan_model.md` untuk ketiga skenario.
6. Commit hasilnya.

## Yang dilatih

- Membaca metadata model: harga, context window, modality, supported parameters.
- Mengubah harga “per token” menjadi “per 1 juta token”.
- Menyaring data JSON dengan beberapa kondisi.
- Menimbang tradeoff: kualitas, biaya, latency, privasi, dan operasional.
- Menulis rekomendasi teknis yang bisa dipertanggungjawabkan.

## Rubrik penilaian

| Kriteria | Pertanyaan |
|---|---|
| Fungsional | 5 fungsi lulus test? |
| Penalaran | Alasan pemilihan model jelas dan terkait constraint? |
| Tradeoff | Menyebut kekurangan, bukan hanya kelebihan? |
| Realistis | Harga/context yang dikutip masuk akal dan sumbernya jelas? |
| Privasi | Skenario sensitif tidak asal pakai API publik? |

## Hasil

- Test: **7/7 lulus** (total repo: 19/19).
- Katalog saat dijalankan: **457 model**; 255 kandidat dengan prompt ≤ $1/juta,
  context ≥ 32k, dan dukungan `response_format`.
- Pelajaran penting: filter metadata saja tidak cukup. Model audio dan
  auto-router bisa lolos filter, jadi modality dan jenis model harus diperiksa.
- Rekomendasi di laporan:
  - **A (chatbot support):** `recursive/flint-v1.0:free` untuk prototipe;
    `openai/gpt-oss-20b` untuk produksi (≈ $0.65/bulan pada 500 chat/hari).
  - **B (kontrak hukum):** `z-ai/glm-5.2` hanya lewat provider zero-retention,
    private cloud, atau self-hosted — bukan API publik biasa.
  - **C (klinik offline):** Llama 3.2 3B Instruct Q4_K_M untuk 8 GB VRAM,
    dengan JSON terbatas + validasi + review dokter.

Laporan lengkap ada di [`laporan_model.md`](laporan_model.md).

## Catatan

- Tidak perlu API key untuk lab ini.
- Harga dan daftar model **berubah**. Kutip tanggal akses di laporan.
- Jangan menempelkan API key ke kode, test, atau laporan.
