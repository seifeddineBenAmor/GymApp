import os, uuid, shutil
from fastapi import UploadFile, HTTPException
from app.core.config import settings

def save_file(file, folder, allowed):
    extension = file.filename.rsplit(".", 1)[-1].lower()
    if extension not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid file type")
    filename = f"{uuid.uuid4()}.{extension}"
    destination = os.path.join(settings.UPLOAD_DIR, folder, filename)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return filename

def delete_file(filename, folder):
    destination = os.path.join(settings.UPLOAD_DIR, folder, filename)
    if os.path.exists(destination):
        os.remove(destination)

