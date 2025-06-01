import cv2
from ocr_utils import perform_ocr, categorize_book # Impor fungsi dari ocr_utils

def show_webcam_with_ocr():
    # Menginisialisasi webcam. Angka 0 biasanya merujuk ke webcam default.
    # Jika kamu punya lebih dari satu webcam, kamu bisa coba angka lain seperti 1, 2, dst.
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Tidak bisa membuka webcam.")
        return

    print("Tekan 'q' untuk keluar dari jendela webcam.")
    print("Tekan 'SPACE' untuk mengambil gambar dan melakukan OCR.")

    while True:
        # Membaca frame demi frame dari webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Tidak bisa menerima frame (stream berakhir?). Keluar ...")
            break

        # Tampilkan frame asli
        cv2.imshow('Webcam Realtime - Tekan Spasi untuk Scan', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord(' '): # Jika tombol spasi ditekan
            print("\nMemproses frame untuk OCR...")
            # Simpan frame saat ini ke file temporer untuk OCR
            # easyocr biasanya mengharapkan path file atau array numpy
            # Untuk kesederhanaan, kita simpan dan baca lagi, mirip dengan capture_frame di ocr_utils
            # tapi kita akan langsung proses array numpy frame jika memungkinkan dan lebih efisien
            # Untuk saat ini, mari kita coba langsung dengan frame (numpy array)
            
            # Melakukan OCR pada frame yang ditangkap (frame adalah gambar dalam format numpy array)
            extracted_text = perform_ocr(frame) # Modifikasi perform_ocr mungkin diperlukan jika ia hanya menerima path

            if extracted_text.strip():
                print(f"Teks yang Diekstrak: {extracted_text}")
                
                # Kategorikan buku berdasarkan teks yang diekstrak
                category = categorize_book(extracted_text)
                print(f"Kategori Buku (Prediksi): {category}")
            else:
                print("Tidak ada teks yang terdeteksi pada frame.")
            print("--------------------------------------------------")

    # Melepaskan webcam dan menutup semua jendela OpenCV
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    show_webcam_with_ocr() 