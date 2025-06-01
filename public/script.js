const video = document.getElementById('video');
const startButton = document.getElementById('startButton');
const scanButton = document.getElementById('scanButton');
const resultsDiv = document.getElementById('results');
const extractedTextSpan = document.getElementById('extractedText');
const bookCategorySpan = document.getElementById('bookCategory');
const loadingDiv = document.getElementById('loading');
let stream;

startButton.onclick = async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        scanButton.disabled = false;
        startButton.disabled = true;
    } catch (err) {
        console.error("Error accessing webcam: ", err);
        alert("Tidak bisa mengakses webcam. Pastikan izin telah diberikan.");
    }
};

scanButton.onclick = async () => {
    loadingDiv.style.display = 'block';
    resultsDiv.style.display = 'none';
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/jpeg');
    const base64Data = dataUrl.split(',')[1];

    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image_data: base64Data }),
        });

        loadingDiv.style.display = 'none';
        if (!response.ok) {
            const errorResult = await response.json();
            throw new Error(errorResult.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.error) {
            extractedTextSpan.textContent = data.error;
            bookCategorySpan.textContent = "N/A";
        } else {
            extractedTextSpan.textContent = data.text || "Tidak ada teks yang terdeteksi.";
            bookCategorySpan.textContent = data.category || "Kategori Tidak Dapat Ditentukan";
        }
        resultsDiv.style.display = 'block';

    } catch (error) {
        console.error('Error during scan:', error);
        loadingDiv.style.display = 'none';
        extractedTextSpan.textContent = `Error: ${error.message}`;
        bookCategorySpan.textContent = "N/A";
        resultsDiv.style.display = 'block';
        alert(`Gagal memproses gambar: ${error.message}`);
    }
};

// Optional: Stop webcam when the page is closed or navigated away from
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
}); 