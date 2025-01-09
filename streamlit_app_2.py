import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import wave
import numpy as np
import datetime

# Audio recorder callback
class AudioRecorderProcessor:
    def __init__(self):
        self.audio_frames = []

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.audio_frames.append(audio)
        return frame

# Streamlit UI
def main():
    st.title("Streamlit Audio Recorder")
    st.write("Press start to record audio.")

    # Initialize WebRTC streamer
    recorder = webrtc_streamer(
        key="audio-recorder",
        media_stream_constraints={"audio": True, "video": False},
        audio_processor_factory=AudioRecorderProcessor,
        mode=WebRtcMode.SENDRECV,
    )

    if recorder and recorder.audio_processor:
        if st.button("Stop and Save Recording"):
            if recorder.audio_processor.audio_frames:
                audio_data = np.concatenate(recorder.audio_processor.audio_frames, axis=0)
                save_audio_file(audio_data)


def save_audio_file(audio_data):
    # Create filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"recording-{timestamp}.wav"

    # Save audio data to .wav file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # Assuming 16-bit samples
        wf.setframerate(16000)
        wf.writeframes(audio_data.tobytes())

    st.success(f"Audio saved as {filename}")


if __name__ == "__main__":
    main()
