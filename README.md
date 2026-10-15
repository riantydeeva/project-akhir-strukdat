# 2EZ4U Food Delivery
_Sebagai Projek Akhir Mata Kuliah Struktur Data & Analisa Algoritma_


## Deskripsi Projek
**2EZ4U Food Delivery** merupakan aplikasi simulasi layanan antar makanan yang berfokus pada penerapan struktur data dan analisis
algoritma dalam pengembangan backend. Aplikasi ini menggunakan data pesanan dan data lokasi yang disimpan dalam format CSV. Data
tersebut diproses melalui enam modul backend yang masing-masing memiliki fungsi berbeda. Untuk memperlihatkan proses kerja backend,
aplikasi menyediakan antarmuka desktop berbasis Tkinter. Pengguna dapat menjalankan operasi melalui antarmuka dan melihat hasilnya,
termasuk waktu eksekusi apabila ditampilkan oleh operasi tersebut.
### Gambaran Umum:
- Nama aplikasi: 2EZ4U Food Delivery
- Kategori: Simulasi layanan antar makanan
- Bahasa pemrograman: Python
- Antarmuka: Tkinter
- Format data: CSV
- Jumlah data: 200.000 baris pesanan
- Arsitektur: Data, backend, dan frontend


## Teknologi yang Digunakan
| Teknologi | Kegunaan |
|---|---|
| Python 3.11+ | Bahasa pemrograman utama |
| Tkinter | Antarmuka desktop |
| CSV | Penyimpanan data pesanan dan peta |
| Git | Pengelolaan versi kode |
| GitHub | Penyimpanan repository dan dokumentasi proyek |


## Struktur Repository
Struktur direktori projek:
```text
2ez4u/
├── .gitignore
├── README.md
│
├── app.py
│
├── data/
│   ├── pesanan.csv
│   └── peta.csv
│
├── backend/
│   ├── m1_pesanan.py
│   ├── m2_antrean.py
│   ├── m3_laporan.py
│
└── frontend/
    └── ui.py
```
### Penjelasan Direktori
- **`app.py`** — Titik masuk utama untuk menjalankan aplikasi.
- **`data/`** — Menyimpan data pesanan dan data lokasi dalam format CSV.
- **`backend/`** — Berisi implementasi struktur data dan algoritma untuk enam milestone.
- **`frontend/`** — Berisi antarmuka pengguna menggunakan Tkinter.
- **`README.md`** — Dokumentasi proyek dan petunjuk penggunaan.
- **`.gitignore`** — Mencegah file yang tidak diperlukan.


## Diagram Arsitektur
Arsitektur aplikasi dibagi menjadi tiga lapisan utama: data, backend, dan frontend.
```text
flowchart TD
    A[Pengguna] --> B[Frontend - Tkinter]
    B --> C[app.py]
    C --> D[Backend]

    D --> M1[M1 - Pesanan]
    D --> M2[M2 - Antrean]
    D --> M3[M3 - Laporan]

    E[(pesanan.csv)] --> M1
    E --> M2
    E --> M3

    M1 --> F[Hasil Operasi]
    M2 --> F
    M3 --> F

    F --> B
```
### Alur Kerja Aplikasi
1. Pengguna menjalankan aplikasi melalui `app.py`.
2. Frontend Tkinter menampilkan menu operasi.
3. Data harus di-load terlebih dahulu agar bisa digunakan.
4. Pengguna memilih operasi yang ingin dilakukan.
5. Backend memproses perintah menggunakan struktur data dan algoritma yang sesuai.
6. Hasil operasi ditampilkan kembali melalui antarmuka.
7. Waktu eksekusi atau informasi performa ditampilkan apabila disediakan oleh operasi tersebut.


## Fitur dan Implementasi
### M1 — Manajemen Pesanan
**File:** `backend/m1_pesanan.py`

Modul ini mengelola data pesanan menggunakan dua struktur data yang berbeda, yaitu array dan linked list.

Fitur utama:
- Melihat daftar dan detail pesanan.
- Menambahkan pesanan reguler, prioritas, dan VIP.
- Menghapus pesanan.
- Membandingkan kinerja array dan linked list.

Aturan penyisipan pesanan:

| Jenis Pesanan | Prioritas | Posisi Penyisipan |
|---|---:|---|
| VIP | 1 | Paling depan |
| Prioritas | 2 | Bagian tengah |
| Reguler | 3 | Paling belakang |

Kedua struktur data digunakan untuk mengolah data yang sama agar perbandingan kinerja dapat dilakukan secara adil.

### M2 — Antrean dan Undo/Redo

**File:** `backend/m2_antrean.py`

Modul ini menerapkan stack dan queue untuk pengelolaan antrean pesanan.

Fitur yang direncanakan dalam spesifikasi:

- Menambahkan pesanan ke antrean (*enqueue*).
- Mengambil pesanan dari antrean (*dequeue*).
- Membandingkan antrean biasa dan antrean melingkar.
- Mengubah ekspresi infix menjadi postfix.
- Mengevaluasi ekspresi postfix.
- Membatalkan operasi menggunakan undo.
- Mengulangi operasi yang dibatalkan menggunakan redo.

### M3 — Sorting dan Searching

**File:** `backend/m3_laporan.py`

Modul ini berfokus pada pengurutan dan pencarian data pesanan.

Algoritma yang menjadi bagian spesifikasi:

- Insertion sort.
- Merge sort.
- Linear search.
- Binary search.

Perbandingan dapat dilakukan menggunakan jumlah perbandingan dan waktu eksekusi untuk memahami perbedaan efisiensi setiap algoritma.


## Cara Menjalankan Aplikasi

### 1. Persyaratan

Pastikan perangkat sudah memiliki:

- Python versi 3.11 atau lebih baru.
- Git, jika ingin mengkloning repository.
- Tkinter yang tersedia pada instalasi Python.
- Seluruh file proyek, termasuk data CSV yang diperlukan.

Periksa versi Python melalui terminal:

```bash
python --version
```

Jika perintah tersebut tidak berfungsi, coba:

```bash
py --version
```

### 2. Clone Repository

```bash
git clone https://github.com/riantydeeva/project-akhir-strukdat
cd project-akhir-strukdat
```

> Ganti `riantydeeva/project-akhir-strukdat` dengan alamat repository GitHub milikmu.

### 3. Periksa Struktur File

Pastikan file utama tersedia:

```text
app.py
backend/
frontend/
data/
```

Pastikan file `pesanan.csv` dan `peta.csv` berada di direktori `data/`.

### 4. Jalankan Aplikasi

Dari direktori utama proyek, jalankan:

```bash
python app.py
```

Pada Windows, kamu juga dapat menggunakan:

```bash
py app.py
```

Jika konfigurasi sudah benar, jendela aplikasi Tkinter akan terbuka.

### 5. Menggunakan Aplikasi

1. Buka aplikasi.
2. Load data terlebih dahulu.
3. Pilih modul atau operasi yang tersedia pada antarmuka.
4. Masukkan parameter jika diperlukan.
5. Jalankan operasi.
6. Periksa hasil yang ditampilkan.
7. Amati informasi waktu eksekusi atau perbandingan performa jika tersedia.

Jika aplikasi tidak dapat dijalankan, periksa pesan kesalahan pada terminal dan pastikan seluruh file serta dependensi yang diperlukan sudah tersedia.


## Struktur Data dan Kompleksitas

Tabel berikut merangkum kompleksitas teoritis beberapa operasi utama berdasarkan struktur data dan algoritma yang digunakan dalam rancangan proyek.

| Struktur Data / Algoritma | Operasi | Kompleksitas Waktu |
|---|---|---|
| Array dinamis | Menambah elemen di belakang | O(1) amortized |
| Array | Mengakses elemen berdasarkan indeks | O(1) |
| Array | Menyisipkan elemen di tengah | O(n) |
| Linked list dengan penunjuk tail | Menambah elemen di belakang | O(1) |
| Linked list | Mengakses elemen berdasarkan indeks | O(n) |
| Linked list | Menyisipkan di depan | O(1) |
| Stack | Push / pop | O(1) |
| Queue melingkar | Enqueue / dequeue | O(1) |
| Insertion sort | Pengurutan | O(n²) terburuk |
| Merge sort | Pengurutan | O(n log n) |
| Linear search | Pencarian | O(n) |
| Binary search | Pencarian pada data terurut | O(log n) |

Keterangan:
- `n` = jumlah elemen data.
- Kompleksitas aktual bergantung pada implementasi yang digunakan.
- Tabel ini menunjukkan kompleksitas teoritis, bukan hasil pengukuran langsung dari aplikasi.

### Analisis Performa

Perbandingan performa sebaiknya dilakukan menggunakan data dan kondisi pengujian yang sama.

Aspek yang dapat diamati meliputi:

- Waktu eksekusi.
- Jumlah perbandingan.
- Jumlah pergeseran elemen.
- Jumlah simpul yang ditelusuri.
- Perbedaan kinerja ketika ukuran data meningkat.

Hasil pengukuran aktual dapat ditambahkan pada bagian ini setelah pengujian dilakukan.


## Format Data
Aplikasi menggunakan file CSV untuk menyimpan data pesanan dan informasi lokasi.
### Data Pesanan — `data/pesanan.csv`

Berdasarkan spesifikasi proyek, data pesanan mencakup informasi berikut:

| Kolom | Keterangan |
|---|---|
| `oid` | ID unik pesanan |
| `pelanggan` | Nama pelanggan |
| `resto` | Nama restoran |
| `menu` | Nama menu |
| `harga` | Harga pesanan |
| `prioritas` | Tingkat prioritas pesanan |
| `t_masuk` | Waktu pesanan masuk dalam detik |
| `t_selesai` | Waktu pesanan selesai dalam detik; dapat kosong jika belum selesai |
| `status` | Status pesanan |

Tingkat prioritas:

- `1` — VIP
- `2` — Prioritas
- `3` — Reguler

Status pesanan pada spesifikasi:

- `DONE` — Pesanan selesai.
- `CANCEL` — Pesanan dibatalkan.
- `ANTRE` — Pesanan masih dalam antrean.

Nama kolom di atas mengikuti istilah spesifikasi proyek. Pastikan nama kolom dan urutannya sesuai dengan implementasi parser CSV pada kode.
