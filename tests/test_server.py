import importlib
import importlib.util
import io
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from starlette.datastructures import UploadFile, Headers


@pytest.fixture
def server_app():
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"text": "hello"}
    fake_whisper = types.SimpleNamespace(load_model=lambda _: mock_model)
    sys.modules['whisper'] = fake_whisper
    # Provide stub for python-multipart to satisfy FastAPI dependency check
    fake_multipart = types.ModuleType("multipart")
    fake_multipart.__version__ = "0"
    multipart_sub = types.ModuleType("multipart.multipart")
    def parse_options_header(value):
        return value, {}
    multipart_sub.parse_options_header = parse_options_header
    fake_multipart.multipart = multipart_sub
    sys.modules['multipart'] = fake_multipart
    sys.modules['multipart.multipart'] = multipart_sub
    spec = importlib.util.spec_from_file_location("server", str(Path(__file__).resolve().parent.parent / "server.py"))
    server = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = server
    spec.loader.exec_module(server)
    yield server
    sys.modules.pop('whisper', None)
    sys.modules.pop('multipart', None)
    sys.modules.pop('multipart.multipart', None)


def test_transcribe_valid_audio(server_app):
    file = UploadFile(
        file=io.BytesIO(b"abc"),
        filename="sample.wav",
        headers=Headers({"content-type": "audio/wav"}),
    )
    import asyncio
    result = asyncio.run(server_app.transcribe(file))
    assert result == {"text": "hello"}


def test_transcribe_invalid_file(server_app):
    file = UploadFile(
        file=io.BytesIO(b"abc"),
        filename="text.txt",
        headers=Headers({"content-type": "text/plain"}),
    )
    import asyncio
    with pytest.raises(HTTPException) as exc:
        asyncio.run(server_app.transcribe(file))
    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid audio file"
