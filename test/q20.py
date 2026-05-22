import io

from flask import send_file
from PIL import Image


@app.route("/image")
def get_image():
    img = Image.new("RGB", (300, 100), "white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")
