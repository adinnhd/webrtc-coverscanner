import cv2
import uvicorn # Keep for local testing if needed, but Vercel handles server
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # For local testing if frontend is on different port
from pydantic import BaseModel
# ocr_utils will be in the same directory in the Vercel environment
from ocr_utils import perform_ocr, categorize_book
import numpy as np
import base64

app = FastAPI()

# Optional: Configure CORS for local development if you serve index.html
# from a different port or using a live server extension.
# For Vercel deployment, this might not be strictly necessary if the 
# frontend and API are on the same Vercel domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for simplicity, restrict in production
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"]
)

class ImageData(BaseModel):
    image_data: str # Base64 encoded image string

@app.post("/api/scan") # Adjusted path for Vercel convention
async def scan_image(image_data: ImageData):
    try:
        img_bytes = base64.b64decode(image_data.image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            raise HTTPException(status_code=400, detail="Gagal memproses gambar. Invalid image data.")

        extracted_text = perform_ocr(frame)
        category = "Kategori Tidak Dapat Ditentukan"
        if extracted_text and extracted_text.strip():
            category = categorize_book(extracted_text)
        
        return {
            "text": extracted_text,
            "category": category
        }

    except HTTPException as e: # Re-raise HTTPException
        raise e
    except Exception as e:
        print(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# This part is for local execution with uvicorn (e.g., python api/index.py)
# Vercel will use its own way to run the FastAPI app as a serverless function.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 