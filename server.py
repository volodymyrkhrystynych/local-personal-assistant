import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
import whisper

app = FastAPI(title="Local STT Server")

model = whisper.load_model("base")  # change to small/medium if hardware allows

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    if not audio.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="Invalid audio file")

    contents = await audio.read()
    # whisper expects a path or file-like object; we use bytes
    # convert bytes to temporary file
    import tempfile

    with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmp:
        tmp.write(contents)
        tmp.flush()
        result = model.transcribe(tmp.name)

    return {"text": result.get("text", "").strip()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
