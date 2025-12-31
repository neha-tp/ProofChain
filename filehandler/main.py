from fastapi import FastAPI, UploadFile, File, HTTPException
from file_handler import handle_uploaded_file

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        result = await handle_uploaded_file(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
