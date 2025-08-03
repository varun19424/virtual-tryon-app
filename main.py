from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
from pathlib import Path
from utils import overlay_clothing_fixed

app = FastAPI()

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.post("/tryon/")
async def tryon(user_img: UploadFile = File(...), cloth_img: UploadFile = File(...)):
    user_path = UPLOAD_DIR / "user.png"
    cloth_path = UPLOAD_DIR / "cloth.png"
    output_path = OUTPUT_DIR / "result.png"

    with open(user_path, "wb") as f:
        shutil.copyfileobj(user_img.file, f)

    with open(cloth_path, "wb") as f:
        shutil.copyfileobj(cloth_img.file, f)

    success = overlay_clothing_fixed(str(user_path), str(cloth_path), str(output_path))

    if success:
        return FileResponse(output_path, media_type="image/png")
    return {"error": "Failed to generate try-on image"}
