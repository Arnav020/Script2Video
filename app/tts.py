# app/tts.py
from pydub.generators import Sine
import os

def script_to_audio(
    script_file="data/sample_script.txt", 
    output_file="outputs/audio/dialogue_stub.wav"
):
    """Convert Script lines to dummy audio beeps (stub)."""

    os.makedirs(os.path.dirname(output_file),exist_ok=True)

    with open(script_file, "r",encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]  # gives a list of scene/dialogue lines

    # 440Hz sine wave = "A" tone
    audio = Sine(440).to_audio_segment(duration=500) # 0.5s per beep

    result =None
    for _ in lines:
        if result is None:
            result = audio
        else:
            result += audio

    if result:
        result.export(output_file,format="wav")
        print(f"Dummy audio saved to {output_file}")
    else:
        print("No text lines found in script")


if __name__=="__main__":
    script_to_audio()