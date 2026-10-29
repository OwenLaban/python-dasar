# Lab Minggu 10 — Ekosistem Model

Tujuan: belajar **memilih model berdasarkan kebutuhan**, bukan berdasarkan
model yang paling ramai dibicarakan.

Lab ini memakai katalog publik OpenRouter (`/api/v1/models`) yang bisa diakses
**tanpa API key**. Kamu akan menyaring model berdasarkan harga, context window,
dan dukungan structured output, lalu menulis rekomendasi untuk tiga skenario.

## File

```text
latihan_model/
├── README.md            # instruksi ini
├── studi_kasus.md       # 3 skenario nyata
├── model_explorer.py    # 5 fungsi TODO
├── test_model_explorer.py
└── laporan_model.md     # template laporan yang kamu isi
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

## Catatan

- Tidak perlu API key untuk lab ini.
- Harga dan daftar model **berubah**. Kutip tanggal akses di laporan.
- Jangan menempelkan API key ke kode, test, atau laporan.
