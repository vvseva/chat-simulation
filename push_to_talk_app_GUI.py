#!/usr/bin/env python
#####################################################################
# Flask web app with a push-to-talk interface to the Realtime API #
# Requires the `OPENAI_API_KEY` environment variable to be set.    #
#####################################################################
#
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "flask",
#     "numpy",
#     "pyaudio",
#     "pydub",
#     "sounddevice",
#     "openai[realtime]",
# ]
#
# [tool.uv.sources]
# openai = { path = "../../", editable = true }
# ///
from __future__ import annotations

import base64
import asyncio
import json
from flask import Flask, render_template, Response, request, jsonify
from typing import Any, cast
from audio_util import CHANNELS, SAMPLE_RATE, AudioPlayerAsync
import sounddevice as sd
from openai import AsyncOpenAI
from openai.types.beta.realtime.session import Session
from openai.resources.beta.realtime.realtime import AsyncRealtimeConnection

app = Flask(__name__)

client: AsyncOpenAI
connection: AsyncRealtimeConnection | None = None
session: Session | None = None
audio_player: AudioPlayerAsync
last_audio_item_id: str | None = None
connected = asyncio.Event()
should_send_audio = asyncio.Event()
is_recording = False
is_paused = False  # Add a flag to track if recording is paused
mic_index = 1  # Choose your microphone index


async def handle_realtime_connection():
    global connection, session, last_audio_item_id, audio_player
    async with client.beta.realtime.connect(
        model="gpt-4o-realtime-preview-2024-10-01"
    ) as conn:
        connection = conn
        connected.set()

        # System prompt
        await conn.conversation.item.create(
            item={
                "type": "message",
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Your Name is Sage. You are an expert in space exploration. And the best landing location is Eridania.",
                    }
                ],
            }
        )

        # Turn detection can be omitted if you want to handle it yourself.
        await conn.session.update(session={"turn_detection": {"type": "server_vad"}})

        acc_items: dict[str, Any] = {}

        async for event in conn:
            if event.type == "session.created":
                session = event.session
                print(f"Session created: {event.session.id}")
            elif event.type == "session.updated":
                session = event.session
            elif event.type == "response.audio.delta":
                if event.item_id != last_audio_item_id:
                    audio_player.reset_frame_count()
                    last_audio_item_id = event.item_id
                bytes_data = base64.b64decode(event.delta)
                audio_player.add_data(bytes_data)
            elif event.type == "response.audio_transcript.delta":
                try:
                    text = acc_items[event.item_id]
                except KeyError:
                    acc_items[event.item_id] = event.delta
                else:
                    acc_items[event.item_id] = text + event.delta
                print(f"Transcript: {acc_items[event.item_id]}")


async def _get_connection() -> AsyncRealtimeConnection:
    await connected.wait()
    assert connection is not None
    return connection


async def send_mic_audio():
    global is_recording, is_paused
    sent_audio = False
    read_size = int(SAMPLE_RATE * 0.02)

    stream = sd.InputStream(
        channels=CHANNELS,
        samplerate=SAMPLE_RATE,
        dtype="int16",
        device=mic_index,
    )
    stream.start()

    try:
        while True:
            if stream.read_available < read_size:
                await asyncio.sleep(0)
                continue
            if not should_send_audio.is_set():
                await asyncio.sleep(0)
                continue

            data, _ = stream.read(read_size)

            if is_paused:
              # If paused, don't send data, but keep reading from stream.
              continue

            is_recording = True
            conn = await _get_connection()

            if not sent_audio:
                asyncio.create_task(conn.send({"type": "response.cancel"}))
                sent_audio = True

            await conn.input_audio_buffer.append(
                audio=base64.b64encode(cast(Any, data)).decode("utf-8")
            )
            await asyncio.sleep(0)

    except Exception as e:
        print(f"Error in send_mic_audio: {e}")
    finally:
        stream.stop()
        stream.close()
        is_recording = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/toggle_pause_recording", methods=["POST"])
async def toggle_pause_recording():
    global is_recording, is_paused
    if not is_recording:
        # Start recording
        should_send_audio.set()
        is_paused = False  # Ensure not paused when starting
    else:
        # Pause or unpause
        is_paused = not is_paused
        if not is_paused:
            # Resuming, so potentially send buffered audio
            pass
        else:
            # Pausing
            if session and session.turn_detection is None:
                # Manual turn detection, so end the turn
                conn = await _get_connection()
                await conn.input_audio_buffer.commit()
                await conn.response.create()
    return jsonify({"is_recording": is_recording, "is_paused": is_paused})

@app.route("/status")
def status():
    if is_recording:
      status_text = "⏸️ Paused" if is_paused else "🔴 Recording..."
    else:
      status_text = "⚪ Ready"
    return jsonify({"status": status_text, "is_paused": is_paused})


async def run_app():
    global client, audio_player
    client = AsyncOpenAI()
    audio_player = AudioPlayerAsync()

    asyncio.create_task(handle_realtime_connection())
    asyncio.create_task(send_mic_audio())

    # Run Flask app in a separate thread
    import threading

    threading.Thread(
        target=lambda: app.run(debug=False, use_reloader=False, port=5000),
        daemon=True,
    ).start()

    # Keep the main thread alive for Ctrl+C handling
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run_app())