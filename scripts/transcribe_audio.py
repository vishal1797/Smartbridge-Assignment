"""
transcribe_audio.py

Stretch-goal script for Part 2.1 of the Smartbridge Gen AI assignment.

This replicates, in Python, what was done manually in the Azure Speech Studio
UI: transcribing a short audio clip using Azure Speech Services (Speech-to-Text).

Setup:
    pip install azure-cognitiveservices-speech

Environment variables required (set these before running, do NOT hardcode keys):
    SPEECH_KEY      - Key 1 from your Azure Speech resource (Keys and Endpoint blade)
    SPEECH_REGION   - Region of your Speech resource, e.g. "eastus"

Usage:
    export SPEECH_KEY="your-key-here"
    export SPEECH_REGION="eastus"
    python transcribe_audio.py path/to/smartbridge-clip.wav transcript.txt

Notes:
    - Input audio should ideally be mono, 16kHz, 16-bit PCM WAV
      (matches what ffmpeg produces with: -ar 16000 -ac 1 -acodec pcm_s16le)
    - This uses continuous recognition so it can handle audio longer than
      Azure's ~60 second single-shot limit.
"""

import os
import sys
import time
import azure.cognitiveservices.speech as speechsdk


def transcribe(audio_path: str, output_path: str) -> None:
    speech_key = os.environ.get("SPEECH_KEY")
    service_region = os.environ.get("SPEECH_REGION")

    if not speech_key or not service_region:
        raise EnvironmentError(
            "Please set SPEECH_KEY and SPEECH_REGION environment variables."
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    all_results = []
    done = False

    def handle_final_result(evt):
        if evt.result.text:
            all_results.append(evt.result.text)
            print(f"Recognized: {evt.result.text}")

    def stop_cb(evt):
        nonlocal done
        print("Transcription session stopped.")
        done = True

    recognizer.recognized.connect(handle_final_result)
    recognizer.session_stopped.connect(stop_cb)
    recognizer.canceled.connect(stop_cb)

    recognizer.start_continuous_recognition()
    while not done:
        time.sleep(0.5)
    recognizer.stop_continuous_recognition()

    full_transcript = " ".join(all_results)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_transcript)

    print(f"\nSaved transcript ({len(full_transcript)} characters) to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transcribe_audio.py <input_audio.wav> <output_transcript.txt>")
        sys.exit(1)

    transcribe(sys.argv[1], sys.argv[2])
