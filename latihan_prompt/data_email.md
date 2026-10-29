# Data Email untuk Latihan Prompt

Gunakan email di bawah ini **apa adanya**. Jangan menambah atau mengurangi isi
saat membandingkan prompt.

---

## Email 1 — Kasus utama

```text
Halo tim support,

Saya Rina dari PT Maju Bersama. Kami berlangganan paket Pro sejak minggu lalu,
tapi sejak kemarin semua anggota tim tidak bisa login. Muncul error "invalid token"
setiap kali mencoba. Saya sudah reset password dua kali, tetap gagal. Ini urgent
karena kami harus mengirim laporan ke klien besok pagi.

Tolong segera dibantu.

Terima kasih,
Rina
```

### Kunci evaluasi Email 1

| Field | Nilai yang diharapkan |
|---|---|
| `nama` | Rina |
| `produk` | Paket Pro |
| `masalah` | Tidak bisa login, error `invalid token`, reset password gagal |
| `urgent` | `true` |
| `prioritas` | `tinggi` — blocking + deadline besok |
| `ringkasan` | Ringkas dan tidak menambah fakta baru |

---

## Email 2 — Edge case

```text
Halo,

Saya mencoba fitur export CSV tapi file yang diunduh kosong. Saya pakai versi
gratis. Tidak terlalu mendesak, tapi mohon dicek. Kalau perlu info tambahan,
beri tahu saya.

Terima kasih,
Budi
```

### Kunci evaluasi Email 2

| Field | Nilai yang diharapkan |
|---|---|
| `nama` | Budi |
| `produk` | Versi gratis |
| `masalah` | Export CSV menghasilkan file kosong |
| `urgent` | `false` |
| `prioritas` | `rendah` atau `sedang` — yang penting **bukan** `tinggi` |
| `ringkasan` | Tidak mengarang penyebab atau solusi |

Email 2 sengaja ambigu. Prompt yang baik harus bisa menangani informasi yang
tidak lengkap tanpa mengarang.

---

## Aturan prioritas

| Prioritas | Kapan dipakai |
|---|---|
| `tinggi` | Pekerjaan terhenti, banyak pengguna terdampak, atau deadline sangat dekat |
| `sedang` | Fitur terganggu, tetapi masih ada workaround |
| `rendah` | Pertanyaan, permintaan non-blocking, atau dampak kecil |
