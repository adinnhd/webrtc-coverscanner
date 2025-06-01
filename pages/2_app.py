import streamlit as st
import cv2
import easyocr
import json
from PIL import Image
import numpy as np

# Inisialisasi OCR
reader = easyocr.Reader(['en', 'id'])

# Fungsi untuk mendapatkan informasi kategori (termasuk rack_id)
def get_category_info(category_name, categories_file="book_categories.json"):
    """Mendapatkan informasi kategori (termasuk rack_id) berdasarkan nama kategori."""
    try:
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
            for category_info in categories_data:
                if category_info.get("category_name") == category_name:
                    return category_info
    except FileNotFoundError:
        st.error("Error: File Kategori Tidak Ditemukan. Pastikan 'book_categories.json' ada.")
    except json.JSONDecodeError:
        st.error("Error: Format File Kategori Salah. Periksa 'book_categories.json'.")
    return None

# Fungsi kategori yang sekarang mengembalikan kategori dan rak
def categorize_book(text, categories_file="book_categories.json"):
    text_lower = text.lower()
    if not text_lower.strip():
        return "Kategori Tidak Dapat Ditentukan (Tidak ada teks)", None

    try:
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
    except FileNotFoundError:
        st.error("Error: File Kategori Tidak Ditemukan. Pastikan 'book_categories.json' ada.")
        return "Error: File Kategori Tidak Ditemukan", None
    except json.JSONDecodeError:
        st.error("Error: Format File Kategori Salah. Periksa 'book_categories.json'.")
        return "Error: Format File Kategori Salah", None

    best_match_category = "Kategori Tidak Diketahui"
    max_score = 0
    for category_info in categories_data:
        current_score = sum(1 for keyword in category_info.get("keywords", []) if keyword.lower() in text_lower)
        if current_score > max_score:
            max_score = current_score
            best_match_category = category_info.get("category_name", "Nama Kategori Tidak Ada")

    # Dapatkan informasi rak setelah kategori terbaik ditemukan
    category_details = get_category_info(best_match_category, categories_file)
    rack_id = category_details.get("rack_id") if category_details else None

    return best_match_category if max_score > 0 else "Kategori Tidak Diketahui (Tidak ada kata kunci cocok)", rack_id


# Inisialisasi session state
if 'camera_on' not in st.session_state:
    st.session_state.camera_on = False
if 'captured_frame' not in st.session_state:
    st.session_state.captured_frame = None

# UI Awal
st.title("🔎 Ayo Mulai Cari Rak Bukumu")
st.write('Untuk memulainya, tekan tombol **"Aktifkan Kamera"** di bawah! 📸')

# Tombol Aktifkan Kamera
if not st.session_state.camera_on:
    if st.button("Aktifkan Kamera"):
        st.session_state.camera_on = True
        st.rerun()
else:
    # Kamera Aktif
    st.subheader("📷 Kamera Aktif - Siapkan Buku Anda")
    frame_placeholder = st.empty()
    scan_button = st.button("📸 Scan Cover Buku")
    stop_camera_button = st.button("🛑 Matikan Kamera")

    # Mulai kamera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Tidak dapat mengakses kamera. Pastikan kamera terhubung dan tidak digunakan oleh aplikasi lain.")
    else:
        ret, frame = cap.read()
        if not ret:
            st.error("Gagal mengambil frame dari kamera. Coba lagi.")
        else:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

            # Simpan frame untuk scanning
            if scan_button:
                st.session_state.captured_frame = frame
                st.success("Gambar berhasil diambil! Lanjut ke proses OCR...")

        cap.release()

    # Tombol Matikan Kamera
    if stop_camera_button:
        st.session_state.camera_on = False
        st.session_state.captured_frame = None
        st.rerun()

# Jika sudah ada hasil gambar yang di-scan
if st.session_state.captured_frame is not None:
    st.subheader("📄 Hasil Scan")
    st.image(st.session_state.captured_frame, channels="BGR", use_container_width=True)

    with st.spinner("🔍 Membaca teks..."):
        frame = st.session_state.captured_frame
        try:
            # Lakukan OCR langsung pada frame (convert BGR ke RGB untuk easyocr)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = reader.readtext(frame_rgb)
            extracted_text = " ".join([text for (_, text, _) in results])

            # Categorize the book and get both category and rack
            kategori, rak = categorize_book(extracted_text)

            st.markdown("### 📝 Teks Terbaca")
            st.write(extracted_text if extracted_text else "Tidak ada teks terbaca.")

            st.markdown("### 🏷️ Kategori Buku")
            st.success(kategori)

            if rak:
                st.markdown(f"### 📍 Rak Buku")
                st.info(f"Buku ini berada di rak: **{rak}**")
            elif kategori != "Kategori Tidak Diketahui (Tidak ada kata kunci cocok)" and kategori != "Kategori Tidak Diketahui" and kategori != "Error: File Kategori Tidak Ditemukan" and kategori != "Error: Format File Kategori Salah":
                st.warning("Informasi rak buku tidak ditemukan untuk kategori ini.")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses gambar: {e}")