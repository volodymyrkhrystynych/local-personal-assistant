import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
import whisper
import torch

app = FastAPI(title="Local STT Server")

def load_best_model() -> "whisper.Whisper":
    """Load the largest Whisper model that fits on the available GPU.

    The function attempts to load models from largest to smallest. If a GPU is
    available, it will use it by default. If loading fails due to memory
    constraints, it falls back to the next smaller model until one succeeds.
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"
    candidates = ["large", "medium", "small", "base", "tiny"]

    for name in candidates:
        try:
            return whisper.load_model(name, device=device)
        except RuntimeError as exc:
            # If the error is related to CUDA memory exhaustion, try a smaller model
            if "out of memory" in str(exc).lower():
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                continue
            raise

    # Fallback to the smallest model if everything else failed
    return whisper.load_model("tiny", device=device)


model = load_best_model()

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
