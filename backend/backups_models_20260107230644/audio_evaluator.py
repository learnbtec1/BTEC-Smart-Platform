try:
    import whisper
    _whisper_available = True
except Exception:
    whisper = None  # type: ignore
    _whisper_available = False

_model = None
if _whisper_available:
    try:
        _model = whisper.load_model("base")
    except Exception:
        _model = None

def transcribe_audio(file_path: str) -> str:
    """Transcribe an audio file using Whisper if available.

    If Whisper is not installed or the model failed to load, this raises
    a RuntimeError to indicate transcription is unavailable.
    """
    if not _whisper_available or _model is None:
        raise RuntimeError("Whisper is not installed or model failed to load; audio transcription unavailable")
    result = _model.transcribe(file_path, language="en")
    return result.get("text", "")