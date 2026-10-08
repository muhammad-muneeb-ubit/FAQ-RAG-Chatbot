# import subprocess
# import tempfile
# from pathlib import Path


# VOICE_MODEL = Path(__file__).parent / "en_US-lessac-medium.onnx"


# def text_to_speech(text: str):

#     if not text or not text.strip():
#         raise ValueError("Text cannot be empty.")

#     if not VOICE_MODEL.exists():
#         raise FileNotFoundError(
#             f"Piper voice model not found: {VOICE_MODEL}"
#         )

#     temp_audio = tempfile.NamedTemporaryFile(
#         suffix=".wav",
#         delete=False
#     )

#     temp_audio.close()

#     output_path = temp_audio.name

#     command = [
#         "python",
#         "-m",
#         "piper",
#         "--model",
#         str(VOICE_MODEL),
#         "--output_file",
#         output_path,
#     ]

#     process = subprocess.run(
#         command,
#         input=text,
#         text=True,
#         capture_output=True,
#     encoding="utf-8"
#     )

#     if process.returncode != 0:
#         raise RuntimeError(
#             f"Piper TTS failed:\n{process.stderr}"
#         )

#     return output_path

# import tempfile
# import wave
# from pathlib import Path

# from piper import PiperVoice # type: ignore


# VOICE_MODEL = Path(__file__).parent / "en_US-lessac-medium.onnx"


# def text_to_speech(text: str):

#     if not text or not text.strip():
#         raise ValueError("Text cannot be empty.")

#     if not VOICE_MODEL.exists():
#         raise FileNotFoundError(
#             f"Piper voice model not found: {VOICE_MODEL}"
#         )

#     output_file = tempfile.NamedTemporaryFile(
#         suffix=".wav",
#         delete=False
#     )

#     output_file.close()

#     output_path = output_file.name

#     voice = PiperVoice.load(str(VOICE_MODEL))

#     with wave.open(output_path, "wb") as wav_file:
#         voice.synthesize_wav(
#             text,
#             wav_file
#         )

#     return output_path



# # text = "NumPy aik Python library hai jo numerical computing ke liye multidimensional arrays aur efficient mathematical operations faraham karti hai."

# # audio_path = text_to_speech(text)

# # print("Audio created:", audio_path)


import subprocess
import tempfile
from pathlib import Path


VOICE_MODEL = Path(__file__).parent / "en_US-lessac-medium.onnx"


def text_to_speech(text: str):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    if not VOICE_MODEL.exists():
        raise FileNotFoundError(
            f"Piper voice model not found: {VOICE_MODEL}"
        )

    temp_audio = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_audio.close()

    output_path = temp_audio.name

    command = [
        "python",
        "-m",
        "piper",
        "--model",
        str(VOICE_MODEL),
        "--output_file",
        output_path,
    ]

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate(
        input=text.encode("utf-8")
    )

    if process.returncode != 0:
        raise RuntimeError(
            f"Piper TTS failed:\n"
            f"{stderr.decode('utf-8', errors='replace')}"
        )

    return output_path