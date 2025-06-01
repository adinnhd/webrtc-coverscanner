import streamlit as st

st.set_page_config(page_title="Panduan Penggunaan", page_icon="📖")

st.title("📖 Panduan Penggunaan Aplikasi")

st.markdown("""
Selamat datang di aplikasi **Pengenalan Sampul Buku untuk Menentukan Rak Pengembalian di Perpustakaan**! 

---

### Apa yang Bisa Aplikasi Ini Lakukan?
Aplikasi ini membantu mengenali **judul atau kata kunci dari cover buku** menggunakan kamera. Setelah teks terbaca, aplikasi mencocokkannya dengan **kategori yang tersedia** (misalnya: Fiksi, Sejarah, Teknologi, dll) menggunakan file `book_categories.json`. Hasilnya bisa digunakan untuk **menentukan rak pengembalian otomatis** di perpustakaan.

---

### Cara Menggunakan:
1. Buka halaman **`app`** di sidebar.
2. Tekan tombol **Aktifkan Kamera** untuk memulai kamera.
3. Arahkan cover buku ke kamera.
4. Tekan tombol **Scan** untuk melakukan deteksi OCR.
5. Aplikasi akan menampilkan hasil teks dari cover buku.
6. Sistem akan mencocokkan teks dengan kategori dari file `book_categories.json`.

---

### Penjelasan Komponen Utama
Berikut ini penjelasan singkat tentang beberapa pustaka penting yang digunakan:

| Library       | Fungsi                                                                 |
|---------------|------------------------------------------------------------------------|
| `easyocr`     | Melakukan OCR (Optical Character Recognition) membaca teks dari gambar cover buku. |
| `cv2`         | Mengelola akses kamera dan mengambil gambar untuk diproses.             |
| `PIL.Image`   | Digunakan untuk memproses dan menampilkan gambar dalam format yang kompatibel dengan Streamlit. |
| `json`        | Membaca dan mencocokkan data dari `book_categories.json`.               |
| `tempfile`    | Menyimpan gambar sementara tanpa perlu menulis ke disk secara permanen. |
---

### Keunggulan Utama Aplikasi
- ➡️ **Real-time camera integration**: Memungkinkan pengguna menangkap gambar langsung dari kamera laptop.
- ➡️ **OCR ringan dan cepat**: Menggunakan EasyOCR tanpa perlu GPU.
- ➡️ **Klasifikasi berbasis teks**: Menggunakan keyword matching dari file JSON yang mudah diubah dan diperluas.
- ➡️ **Streamlit UI sederhana dan intuitif**: Bisa langsung digunakan tanpa instalasi rumit.
- ➡️ **Performa efisien**: OCR hanya dipanggil saat tombol Scan ditekan.

---

### Catatan Tambahan:
- OCR hanya dilakukan saat tombol **Scan** ditekan agar performa lebih ringan.
- Pastikan pencahayaan cukup agar teks dapat terbaca dengan baik.

Selamat mencoba! 🚀
""")
