from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import uuid
from qrscan import compare_images

app = FastAPI()

@app.post('/api/upload-id')
async def upload_id(file: UploadFile = File(...)):
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    filename = f"{uuid.uuid4()}_{os.path.basename(file.filename)}"
    save_path = os.path.join(uploads_dir, filename)
    try:
        content = await file.read()
        with open(save_path, 'wb') as out:
            out.write(content)
        match = compare_images(save_path)
    except Exception as e:
        try:
            os.remove(save_path)
        except Exception:
            pass
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)
    try:
        os.remove(save_path)
    except Exception:
        pass
    return {"ok": True, "match": bool(match)}
