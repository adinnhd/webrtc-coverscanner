import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av
import cv2
import numpy as np
from ocr_utils import perform_ocr, categorize_book
import threading # Untuk menangani state antar callback

# RTCConfiguration untuk deployment (opsional, bisa diperlukan di beberapa environment)
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

# Global variable atau session state untuk menyimpan hasil OCR dan kategori
# Ini cara sederhana, untuk aplikasi lebih kompleks, pertimbangkan st.session_state
class OCRContext:
    def __init__(self):
        self.extracted_text = None
        self.book_category = None
        self.frame_to_process = None
        self.lock = threading.Lock() # Untuk sinkronisasi akses ke frame_to_process

ocr_context = OCRContext()

class OCRVideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame_lock = threading.Lock()
        self.latest_frame = None

    def transform(self, frame: av.VideoFrame) -> np.ndarray:
        img = frame.to_ndarray(format="bgr24")
        with self.frame_lock:
            self.latest_frame = img
        return img # Kembalikan frame asli untuk ditampilkan

    def get_latest_frame(self):
        with self.frame_lock:
            return self.latest_frame.copy() if self.latest_frame is not None else None

def main():
    st.set_page_config(page_title="Webcam OCR with Streamlit", layout="wide")
    st.title("Realtime Book Cover Scanner")
    st.markdown("Arahkan sampul buku ke webcam dan tekan tombol 'Scan Sampul Buku' di bawah.")

    webrtc_ctx = webrtc_streamer(
        key="webcam",
        video_transformer_factory=OCRVideoTransformer,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if st.button("Scan Sampul Buku", key="scan_button"):
        if webrtc_ctx.video_transformer:
            frame_to_scan = webrtc_ctx.video_transformer.get_latest_frame()
            if frame_to_scan is not None:
                st.image(frame_to_scan, channels="BGR", caption="Frame yang Dipindai")
                
                with st.spinner("Sedang memproses OCR..."):
                    # Lakukan OCR pada frame yang diambil
                    text_result = perform_ocr(frame_to_scan)
                    category_result = "Kategori Tidak Dapat Ditentukan" # Default

                    if text_result and text_result.strip():
                        category_result = categorize_book(text_result)
                        ocr_context.extracted_text = text_result
                        ocr_context.book_category = category_result
                    else:
                        ocr_context.extracted_text = "Tidak ada teks yang terdeteksi."
                        ocr_context.book_category = "N/A"
                
                st.success("Pemindaian Selesai!")
            else:
                st.warning("Tidak ada frame yang diterima dari webcam. Pastikan webcam aktif.")
        else:
            st.error("Komponen webcam belum siap. Silakan refresh halaman.")

    if ocr_context.extracted_text:
        st.subheader("Hasil Pemindaian:")
        st.text_area("Teks yang Diekstrak:", ocr_context.extracted_text, height=150)
        st.info(f"Prediksi Kategori Buku: **{ocr_context.book_category}**")

    st.sidebar.header("Tentang Aplikasi")
    st.sidebar.info(
        "Aplikasi ini menggunakan EasyOCR untuk mengekstrak teks dari sampul buku via webcam "
        "dan mengkategorikannya berdasarkan kata kunci."
    )

if __name__ == "__main__":
    main() 