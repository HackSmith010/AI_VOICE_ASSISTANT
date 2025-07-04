from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        lang = request.form.get("lang", "en")

        filename = f"tts_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)

        return send_file(filename, as_attachment=False)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
