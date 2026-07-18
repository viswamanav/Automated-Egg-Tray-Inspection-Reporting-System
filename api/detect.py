from fastapi import APIRouter, UploadFile, File, HTTPException
import traceback

from api.detector import inspect_image

router = APIRouter()


@router.post("/detect")
async def detect(file: UploadFile = File(...)):

    try:
        image_bytes = await file.read()
        return inspect_image(image_bytes, file.filename)
    

    except Exception as e:
        traceback.print_exc()   # Prints the full error in the terminal
        raise HTTPException(status_code=500, detail=str(e))