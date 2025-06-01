# 📚 Cover Book Recognition App

Aplikasi Streamlit untuk melakukan **OCR (Optical Character Recognition)** dari cover buku dan mengklasifikasikannya berdasarkan kategori menggunakan data dari file JSON.

## 🚀 Fitur

- Menyalakan kamera untuk menangkap gambar cover buku.
- Menggunakan OCR untuk mengekstrak teks dari gambar.
- Mencocokkan hasil teks dengan kategori buku dari file JSON.
- Tampilan antarmuka sederhana dan interaktif berbasis Streamlit.
- Halaman panduan penggunaan (Welcome Page) tersedia di sidebar.

---

## 🛠️ Instalasi

Ikuti langkah-langkah berikut untuk menjalankan proyek ini secara lokal.

### 1. Clone Repository

```bash
git clone https://github.com/destyasti/cover-book-recognition.git
cd cover-book-recognition
```

### 2. (Opsional) Buat dan Aktifkan Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Menjalankan Aplikasi

Jalankan aplikasi dengan perintah berikut:

```bash
streamlit run Cover_Book_App.py
```

> File utama `Cover_Book_App.py` akan secara otomatis membuka halaman `Welcome`.

---

## 📁 Struktur Folder

```
cover-book-recognition/
├── pages/
│   ├── 1_welcome.py         # Halaman panduan penggunaan
│   └── 2_app.py             # Halaman utama untuk scan buku
├── book_categories.json     # Dataset kategori buku
├── Cover_Book_App.py        # Entry point aplikasi
├── ocr_utils.py             # Fungsi utilitas untuk OCR
├── requirements.txt         # Daftar dependensi
└── README.md                # Dokumentasi proyek
```

---

## 📝 Catatan

- Aplikasi ini membutuhkan akses kamera perangkat Anda.
- Pastikan browser mengizinkan akses kamera.
- Uji OCR dalam kondisi pencahayaan yang baik untuk hasil maksimal.
