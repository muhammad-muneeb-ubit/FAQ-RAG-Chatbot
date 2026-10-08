from faster_whisper import WhisperModel #type: ignore
import tempfile
import os
# print("\nLoading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("\nModel loaded successfully!")


def transcribe_audio(audio_path):
    segments, info = model.transcribe(
        audio_path,
        beam_size=5
    )

    print("\nDetected language:", info.language)
    print("\nLanguage probability:", info.language_probability)

    transcript = ""

    for segment in segments:
        # print(
        #     f"\n[{segment.start:.2f}s -> {segment.end:.2f}s] "
        #     f"{segment.text}"
        # )

        transcript += segment.text

    return transcript.strip()

# audio_path = "./test_audios/test-1.mp3"
# text = transcribe_audio(audio_path)
# print("\n\nFinal transcript:")
# print(text)

def transcribe_audio_bytes(audio_bytes):
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_audio:

            temp_audio.write(audio_bytes)
            temp_path = temp_audio.name

        transcription = transcribe_audio(temp_path)
    except Exception as e:
        print(f"Error occurred while transcribing audio: {e}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    return transcription



