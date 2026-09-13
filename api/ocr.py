from fastapi import APIRouter, UploadFile, File

from services.ocr_service import read_text


router = APIRouter(
    prefix="/ocr",
    tags=["OCR"]
)


@router.get("/test")
def ocr_test():
    return {
        "status": "success",
        "message": "OCR API is working"
    }


@router.post("/read")
async def read_image_text(file: UploadFile = File(...)):

    # Read uploaded image
    image_data = await file.read()

    # Temporary image file
    image_path = "temp_ocr_image.jpg"

    # Save image
    with open(image_path, "wb") as f:
        f.write(image_data)

    # Run OCR
    result = read_text(image_path)

    return {
        "filename": file.filename,
        "text": result["text"],
        "message": result["message"]
    }