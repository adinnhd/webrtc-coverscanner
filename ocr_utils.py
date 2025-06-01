import easyocr
import cv2
import json
import tempfile
import os

# Construct the absolute path to the directory containing this script
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_BOOK_CATEGORIES_FILE = os.path.join(_CURRENT_DIR, "book_categories.json")

# Inisialisasi Reader hanya sekali
reader = easyocr.Reader(['en', 'id'])

def capture_frame():
    """Ambil satu frame dari kamera dan simpan sebagai file gambar sementara"""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None, "Gagal mengambil gambar dari kamera."

    # Simpan ke file temporer
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    cv2.imwrite(temp_file.name, frame)

    return temp_file.name, None

def perform_ocr(image_input):
    """Melakukan OCR pada file gambar atau array NumPy gambar."""
    # image_input bisa berupa path string ke file atau array NumPy
    results = reader.readtext(image_input)
    extracted_text = " ".join([text for (_, text, _) in results])
    return extracted_text

def get_category_info(category_name, categories_file=_BOOK_CATEGORIES_FILE):
    """Mendapatkan informasi kategori (termasuk rack_id) berdasarkan nama kategori."""
    try:
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
            for category_info in categories_data:
                if category_info.get("category_name") == category_name:
                    return category_info
    except FileNotFoundError:
        print("Error: File Kategori Tidak Ditemukan")
    except json.JSONDecodeError:
        print("Error: Format File Kategori Salah")
    return None

def categorize_book(text, categories_file=_BOOK_CATEGORIES_FILE):
    text_lower = text.lower()
    if not text_lower.strip():
        return "Kategori Tidak Dapat Ditentukan (Tidak ada teks)", None

    try:
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
    except FileNotFoundError:
        return f"Error: File Kategori Tidak Ditemukan di {os.path.abspath(categories_file)}", None
    except json.JSONDecodeError:
        return "Error: Format File Kategori Salah", None

    best_match_category = "Kategori Tidak Diketahui"
    max_score = 0

    for category_info in categories_data:
        current_score = sum(1 for keyword in category_info.get("keywords", []) if keyword.lower() in text_lower)
        if current_score > max_score:
            max_score = current_score
            best_match_category = category_info.get("category_name", "Nama Kategori Tidak Ada")

    category_details = get_category_info(best_match_category, categories_file=categories_file)
    rack_id = category_details.get("rack_id") if category_details else None

    return best_match_category if max_score > 0 else "Kategori Tidak Diketahui (Tidak ada kata kunci cocok)", rack_id

if __name__ == "__main__":
    image_file, error = capture_frame()
    if error:
        print(error)
    elif image_file:
        try:
            print(f"Gambar diambil: {image_file}")
            extracted_text = perform_ocr(image_file)
            print(f"Teks hasil OCR: {extracted_text}")
            category, rack = categorize_book(extracted_text)
            print(f"Kategori buku: {category}")
            if rack:
                print(f"Rak buku: {rack}")
            else:
                print("Informasi rak buku tidak tersedia untuk kategori ini.")
        finally:
            # Hapus file sementara
            if os.path.exists(image_file):
                os.remove(image_file)
                print(f"File sementara dihapus: {image_file}")