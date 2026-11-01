"""Kumpulan 20 kalimat dan query untuk latihan semantic search.

Kalimat sengaja memakai kata yang tidak selalu sama dengan query. Tujuannya
agar terlihat apakah embedding menangkap **makna**, bukan hanya kecocokan kata.
"""

KALIMAT = [
    # Teknologi
    {
        "teks": "Python adalah bahasa pemrograman yang populer untuk membangun aplikasi web.",
        "topik": "teknologi",
    },
    {
        "teks": "Docker membantu mengemas aplikasi agar berjalan sama di berbagai komputer.",
        "topik": "teknologi",
    },
    {
        "teks": "Git menyimpan riwayat perubahan kode dan memudahkan kolaborasi tim.",
        "topik": "teknologi",
    },
    {
        "teks": "API memungkinkan dua program saling bertukar data.",
        "topik": "teknologi",
    },
    {
        "teks": "Model bahasa besar dapat menghasilkan teks dari sebuah instruksi.",
        "topik": "teknologi",
    },
    # Kuliner
    {
        "teks": "Sambal bawang dibuat dari cabai, bawang putih, dan minyak panas.",
        "topik": "kuliner",
    },
    {
        "teks": "Rendang dimasak perlahan dengan santan dan rempah hingga kuahnya mengering.",
        "topik": "kuliner",
    },
    {
        "teks": "Bakso disajikan dengan kuah kaldu hangat dan mie kuning.",
        "topik": "kuliner",
    },
    {
        "teks": "Kopi arabika memiliki aroma khas dan tingkat keasaman yang tinggi.",
        "topik": "kuliner",
    },
    {
        "teks": "Nasi goreng sering disantap dengan telur mata sapi dan kerupuk.",
        "topik": "kuliner",
    },
    # Olahraga
    {
        "teks": "Jogging pagi membantu menjaga kebugaran jantung dan paru-paru.",
        "topik": "olahraga",
    },
    {
        "teks": "Sepeda statis sering dipakai untuk latihan kardio di rumah.",
        "topik": "olahraga",
    },
    {
        "teks": "Pemanasan sebelum olahraga mengurangi risiko cedera otot.",
        "topik": "olahraga",
    },
    {
        "teks": "Renang melatih hampir seluruh otot tubuh tanpa membebani sendi.",
        "topik": "olahraga",
    },
    {
        "teks": "Tim sepak bola itu menang melalui gol di menit akhir.",
        "topik": "olahraga",
    },
    # Keuangan
    {
        "teks": "Dana darurat sebaiknya disimpan di rekening yang mudah diakses.",
        "topik": "keuangan",
    },
    {
        "teks": "Investasi saham memiliki risiko fluktuasi harga yang tinggi.",
        "topik": "keuangan",
    },
    {
        "teks": "Bunga majemuk membuat tabungan tumbuh lebih cepat dalam jangka panjang.",
        "topik": "keuangan",
    },
    {
        "teks": "Asuransi kesehatan membantu menutup biaya pengobatan yang mahal.",
        "topik": "keuangan",
    },
    {
        "teks": "Anggaran bulanan membantu mengendalikan pengeluaran rumah tangga.",
        "topik": "keuangan",
    },
]

QUERY = [
    {
        "teks": "bagaimana memulai karier sebagai programmer",
        "topik": "teknologi",
    },
    {
        "teks": "makanan hangat berkuah untuk makan siang",
        "topik": "kuliner",
    },
    {
        "teks": "olahraga ringan yang aman untuk pemula",
        "topik": "olahraga",
    },
    {
        "teks": "cara mengelola uang agar tidak cepat habis",
        "topik": "keuangan",
    },
]
