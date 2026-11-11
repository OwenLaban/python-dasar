"""Dataset 100 dokumen Indonesia dengan metadata, plus 6 query semantic.

Dokumen dibuat dari 5 kategori, masing-masing 20 kalimat. Metadata
(level, tahun, tag) dibuat otomatis agar varies dan bisa dipakai untuk
mencoba metadata filter di vector database.
"""

LEVEL = ["dasar", "menengah", "lanjut"]
TAHUN = [2023, 2024, 2025]

TEKS: dict[str, list[str]] = {
    "teknologi": [
        "Python adalah bahasa pemrograman yang mudah dipelajari untuk pemula.",
        "Git menyimpan riwayat perubahan kode pada proyek perangkat lunak.",
        "Docker membantu mengemas aplikasi agar konsisten di berbagai komputer.",
        "API adalah antarmuka yang memungkinkan dua aplikasi bertukar data.",
        "Basis data relasional menyimpan tabel dengan hubungan antar data.",
        "JavaScript digunakan untuk membuat interaksi dinamis pada halaman web.",
        "Terminal adalah antarmuka baris perintah untuk menjalankan program.",
        "Compiler mengubah kode sumber menjadi bahasa yang bisa dijalankan mesin.",
        "Server web menerima permintaan HTTP lalu mengembalikan halaman atau data.",
        "Version control membantu melacak perubahan dan memulihkan versi sebelumnya.",
        "Algoritma pengurutan mengubah data acak menjadi terurut sesuai aturan.",
        "Machine learning membuat komputer belajar pola dari data contoh.",
        "Framework frontend memudahkan developer menyusun antarmuka pengguna.",
        "Debugger membantu menemukan penyebab program error saat berjalan.",
        "Antarmuka REST banyak dipakai untuk menghubungkan aplikasi mobile dengan server.",
        "Pengelompokan data mengelompokkan item yang punya ciri serupa.",
        "Sensor IoT mengumpulkan data fisik lalu mengirimkannya ke server.",
        "Virtual machine menjalankan sistem operasi di dalam komputer lain.",
        "Cache menyimpan hasil perhitungan agar tidak perlu diulang.",
        "Pipeline CI otomatis menguji kode setiap kali ada perubahan.",
    ],
    "kesehatan": [
        "Tidur cukup tujuh sampai delapan jam membantu tubuh memulihkan diri.",
        "Minum air putih secara rutin menjaga hidrasi dan metabolisme.",
        "Sayur dan buah segar menyediakan vitamin serta serat bagi tubuh.",
        "Olahraga ringan seperti berjalan kaki tiga puluh menit menjaga kebugaran jantung.",
        "Pemanasan sebelum olahraga mengurangi risiko cedera otot.",
        "Pemeriksaan dokter secara berkala membantu mendeteksi penyakit lebih awal.",
        "Antibiotik harus digunakan sesuai resep agar bakteri tidak kebal.",
        "Stres berkepanjangan dapat meningkatkan tekanan darah.",
        "Masker membantu melindungi diri dari debu dan percikan air.",
        "Kurang tidur menurunkan daya tahan tubuh dan konsentrasi kerja.",
        "Konsumsi gula berlebihan meningkatkan risiko diabetes tipe dua.",
        "Merokok meningkatkan risiko penyakit paru-paru dan jantung.",
        "Makanan tinggi kalium membantu menjaga keseimbangan tekanan darah.",
        "Vaksinasi melindungi anak dari penyakit berbahaya sejak usia dini.",
        "Dehidrasi menyebabkan sakit kepala dan kelelahan pada siang hari.",
        "Jalan kaki di pagi hari membantu menjaga berat badan ideal.",
        "Penyakit kronis perlu pemantauan dokter secara berkala.",
        "Asupan protein membantu regenerasi otot setelah olahraga.",
        "Jam tidur teratur mendukung metabolisme yang sehat dan konsisten.",
        "Kebersihan lingkungan membantu mencegah penyakit yang menular.",
    ],
    "keuangan": [
        "Dana darurat sebaiknya disimpan di rekening yang mudah dicairkan.",
        "Investasi saham memiliki risiko fluktuasi harga yang tinggi.",
        "Bunga majemuk membuat tabungan tumbuh lebih cepat dalam jangka panjang.",
        "Asuransi kesehatan membantu menutup biaya pengobatan yang mahal.",
        "Anggaran bulanan membantu mengendalikan pengeluaran rumah tangga.",
        "Menunda pembelian besar mengurangi beban hutang kartu kredit.",
        "Menyisihkan sebagian penghasilan setiap bulan membentuk kebiasaan menabung.",
        "Inflasi menurunkan daya beli uang dari tahun ke tahun.",
        "Perhitungan untung rugi membantu menilai kesehatan usaha.",
        "Pajak penghasilan dipotong dari gaji setiap bulan.",
        "Reksa dana cocok untuk pemula yang ingin investasi dengan risiko rendah.",
        "Utang kartu kredit berbunga tinggi sebaiknya dilunasi segera.",
        "Tabungan berjangka baru bisa dicairkan setelah tanggal tertentu.",
        "Premi asuransi dibayar rutin agar polis tetap aktif.",
        "Mencatat pengeluaran harian membantu menemukan kebiasaan boros.",
        "Kenaikan harga barang mengurangi daya beli uang yang disimpan.",
        "Dana pensiun sebaiknya disiapkan sejak dini agar cukup saat pensiun.",
        "Rekening berbunga memberikan imbal hasil lebih besar daripada giro biasa.",
        "Target menabung yang jelas membuat kebiasaan menabung lebih konsisten.",
        "Pinjaman dengan bunga tetap membantu perhitungan angsuran.",
    ],
    "pendidikan": [
        "Latihan soal rutin membantu siswa memahami konsep dasar.",
        "Metode belajar aktif membuat siswa lebih cepat memahami materi.",
        "Catatan ringkas setelah pelajaran memudahkan tinjauan ulang.",
        "Umpan balik guru menunjukkan bagian yang perlu diperbaiki siswa.",
        "Belajar kelompok melatih siswa berbagi penjelasan dengan teman.",
        "Hasil ujian memberi gambaran bagian materi yang belum dikuasai.",
        "Membaca buku nonfiksi membantu menambah pengetahuan umum.",
        "Konsentrasi menurun bila suara di kelas terlalu gaduh.",
        "Jadwal belajar yang konsisten lebih efektif daripada belajar dadakan.",
        "Materi yang dicatat dengan tangan lebih mudah diingat.",
        "Kolaborasi tugas kelompok melatih tanggung jawab dan komunikasi.",
        "Presentasi di depan kelas melatih kemampuan berbicara di depan umum.",
        "Catatan kaki di buku membantu mengingat poin penting saat belajar.",
        "Kuis berkala menunjukkan perkembangan belajar dari waktu ke waktu.",
        "Rencana belajar mingguan membuat target belajar terasa lebih mudah.",
        "Bahasa asing yang digunakan sehari-hari menambah kosakata baru.",
        "Perpustakaan sekolah menyediakan buku referensi yang lengkap.",
        "Orang tua dapat mendukung belajar dengan menyediakan waktu dan suasana tenang.",
        "Motivasi belajar meningkat ketika kemajuan terlihat jelas.",
        "Peran guru dalam membentuk kebiasaan belajar sangat penting.",
    ],
    "lingkungan": [
        "Menanam pohon membantu menyerap karbon dioksida dari udara.",
        "Mendaur ulang barang yang masih layak pakai mengurangi sampah.",
        "Energi matahari bisa dipasang sebagai listrik rumah tangga.",
        "Menjaga kebersihan sungai dimulai dari membuang sampah pada tempatnya.",
        "Hemat energi dengan lampu LED mengurangi konsumsi listrik.",
        "Transportasi umum mengurangi polusi udara di kota.",
        "Lahan hijau di sekitar rumah membantu menurunkan suhu udara.",
        "Banjir terjadi ketika saluran air tersumbat oleh sampah.",
        "Ruang hijau di kota memberi tempat bagi warga untuk beristirahat.",
        "Hutan bakau di pesisir laut berfungsi sebagai penahan gelombang tinggi.",
        "Komposting sisa makanan menghasilkan humus untuk tanaman.",
        "Bahan bangunan dari bambu lebih ramah lingkungan daripada beton.",
        "Gotong royong warga membantu kebersihan lingkungan tetap terjaga.",
        "Menggunakan tas belanja mengurangi penggunaan plastik sekali pakai.",
        "Perluasan taman kota membuat suhu udara lebih sejuk.",
        "Penangkapan air hujan mengurangi kebutuhan air PAM saat kemarau.",
        "Limbah organik diolah menjadi humus melalui proses pengomposan.",
        "Pembangkit listrik tenaga surya cocok untuk daerah dengan paparan matahari tinggi.",
        "Berkurangnya penebangan hutan membantu mengurangi perubahan iklim.",
        "Edukasi lingkungan sejak dini membentuk kebiasaan yang lebih sadar lingkungan.",
    ],
}

QUERY = [
    {
        "teks": "tips agar badan tetap sehat setiap hari",
        "kategori": "kesehatan",
    },
    {
        "teks": "belajar pemrograman untuk orang yang baru mulai",
        "kategori": "teknologi",
    },
    {
        "teks": "cara mengatur uang bulanan supaya tidak cepat habis",
        "kategori": "keuangan",
    },
    {
        "teks": "strategi belajar agar nilai ujian membaik",
        "kategori": "pendidikan",
    },
    {
        "teks": "kebersihan lingkungan di sekitar tempat tinggal",
        "kategori": "lingkungan",
    },
    {
        "teks": "menyimpan data aplikasi di server yang bisa diakses",
        "kategori": "teknologi",
    },
]


def build_dokumen() -> list[dict]:
    """Bangun 100 dokumen lengkap dengan metadata yang varies.

    Setiap dokumen punya field: ``id``, ``teks``, ``kategori``, ``level``,
    ``tahun``, dan ``tag`` (list).
    """
    dokumen = []

    for kategori, daftar_teks in TEKS.items():
        for nomor, teks in enumerate(daftar_teks, start=1):
            level = LEVEL[(nomor - 1) % len(LEVEL)]
            tahun = TAHUN[(nomor - 1) % len(TAHUN)]
            dokumen.append(
                {
                    "id": f"{kategori[:3]}-{nomor:02d}",
                    "teks": teks,
                    "kategori": kategori,
                    "level": level,
                    "tahun": tahun,
                    "tag": [kategori, level],
                }
            )

    return dokumen


if __name__ == "__main__":
    semua = build_dokumen()
    print(f"Total dokumen: {len(semua)}")
    print(f"Kategori: {sorted({d['kategori'] for d in semua})}")
    print(f"Contoh: {semua[0]}")
