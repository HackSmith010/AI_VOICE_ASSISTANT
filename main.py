from flask import Flask, render_template, request, Response
import edge_tts
import asyncio
import io

app = Flask(__name__)
VOICE = "en-US-GuyNeural"  # You can change to any voice supported by edge-tts

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text")
    audio_bytes = asyncio.run(text_to_speech(text))
    return Response(audio_bytes, mimetype="audio/mpeg")

async def text_to_speech(text):
    stream = io.BytesIO()
    communicate = edge_tts.Communicate(text, VOICE)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            stream.write(chunk["data"])
    stream.seek(0)
    return stream.read()

if __name__ == "__main__":
    app.run(debug=True)
