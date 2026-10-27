# Prompt Lab — Minggu 8

Isi semua bagian yang bertanda `TODO`. Gunakan **Email 1** untuk kelima variasi,
lalu **Email 2** hanya untuk prompt terbaik.

## Schema output

```json
{
  "nama": "string",
  "produk": "string | null",
  "masalah": "string",
  "urgent": true,
  "prioritas": "rendah | sedang | tinggi",
  "ringkasan": "string"
}
```

Aturan:

- Output hanya JSON valid, tanpa teks pembuka/penutup.
- Jangan mengarang data. Jika tidak ada, gunakan `null`.
- `urgent` dan `prioritas` harus konsisten dengan isi email.

---

# 1. Lima Variasi Prompt

## Prompt 1 — Zero-shot baseline

Fokus: instruksi tugas + email, tanpa contoh dan tanpa role.

```text
[TODO: tulis prompt 1 di sini]
```

## Prompt 2 — Role + schema + constraints

Fokus: beri peran, schema JSON eksplisit, dan aturan output.

```text
[TODO: tulis prompt 2 di sini]
```

## Prompt 3 — Few-shot

Fokus: beri 1–2 contoh input/output sebelum email target. Contoh boleh fiktif,
tetapi formatnya harus sama.

```text
[TODO: tulis prompt 3 di sini]
```

## Prompt 4 — Reasoning / chain-of-thought

Fokus: minta model menilai urgensi dan prioritas secara bertahap, lalu tetap
output **JSON saja**. Bandingkan apakah akurasinya lebih baik dari prompt 2.

```text
[TODO: tulis prompt 4 di sini]
```

## Prompt 5 — Robust + edge case

Fokus:

- batasi email dengan delimiter, misalnya `<email>...</email>`;
- larang model mengikuti instruksi yang ada di dalam email;
- atur penggunaan `null`;
- minta model memeriksa ulang JSON sebelum menjawab.

```text
[TODO: tulis prompt 5 di sini]
```

---

# 2. Output Mentah — Email 1

Tempel output apa adanya dari chatbot.

## Output Prompt 1

```text
[TEMPEL OUTPUT]
```

## Output Prompt 2

```text
[TEMPEL OUTPUT]
```

## Output Prompt 3

```text
[TEMPEL OUTPUT]
```

## Output Prompt 4

```text
[TEMPEL OUTPUT]
```

## Output Prompt 5

```text
[TEMPEL OUTPUT]
```

---

# 3. Tabel Evaluasi — Email 1

| Variasi | JSON valid? | Hanya JSON? | Field lengkap? | Akurasi | Halusinasi? | Catatan |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |

---

# 4. Uji Edge Case — Email 2

Prompt terbaik: **...**

## Output

```text
[TEMPEL OUTPUT]
```

## Evaluasi

| Field | Output | Benar? |
|---|---|---|
| `nama` |  |  |
| `produk` |  |  |
| `masalah` |  |  |
| `urgent` |  |  |
| `prioritas` |  |  |
| `ringkasan` |  |  |

- Apakah model mengarang informasi? ...
- Apakah `prioritas` tetap masuk akal? ...

---

# 5. Refleksi

1. Variasi mana yang paling baik? Mengapa?
2. Apa efek memberi **role + schema**?
3. Apa efek **few-shot**?
4. Apakah **reasoning/CoT** membantu, atau justru merusak format?
5. Apa yang akan kamu ubah dari prompt terbaik?
6. Pelajaran terpenting tentang prompt engineering:
