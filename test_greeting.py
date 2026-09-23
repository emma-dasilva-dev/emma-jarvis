from pathlib import Path
import sys

AUDIO_FILE = Path(__file__).resolve().parent / "assets" / "adrien-jarvis.wav"


def play_greeting() -> None:
    if not AUDIO_FILE.is_file():
        raise FileNotFoundError(f"Audio de Jarvis introuvable : {AUDIO_FILE}")

    if sys.platform == "win32":
        import winsound

        winsound.PlaySound(str(AUDIO_FILE), winsound.SND_FILENAME)
        return

    import wave
    import numpy as np
    import sounddevice as sd

    with wave.open(str(AUDIO_FILE), "rb") as audio:
        channels = audio.getnchannels()
        sample_width = audio.getsampwidth()
        sample_rate = audio.getframerate()
        raw_audio = audio.readframes(audio.getnframes())

    if sample_width != 2:
        raise ValueError("Le fichier WAV doit être en audio 16 bits.")

    samples = np.frombuffer(raw_audio, dtype=np.int16)
    if channels > 1:
        samples = samples.reshape(-1, channels)

    audio_data = samples.astype(np.float32) / 32768.0
    sd.play(audio_data, sample_rate)
    sd.wait()


if __name__ == "__main__":
    print("Lecture du message de Jarvis...")
    play_greeting()
