import logging
import aiohttp
import asyncio
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==========================
# 🔧 CONFIG
# ==========================
BOT_TOKEN = "7633547729:AAF1g6SFjtGjYuIIv417o3YAuZAFvRw46Eg"
API_URL = "https://bot-php-39gd.onrender.com/handle.php"   # PHP API của bạn
MAX_LINES = 30                                              # Giới hạn tối đa 30 dòng / file
DELAY_BETWEEN_CHECKS = 1.5                                  # Thời gian delay giữa mỗi request

# ==========================
# 📜 LOGGING
# ==========================
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==========================
# ⚙️ COMMANDS
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Chào mừng bạn!\n"
        "Gửi file `.txt` có định dạng:\n\n"
        "`username|password`\n"
        "`user2|pass2`\n\n"
        "Mỗi dòng 1 tài khoản.\n"
        "⚠️ Tối đa 30 dòng/lần.\n"
        "Bot sẽ kiểm tra và gửi kết quả."
    )

# ==========================
# 📁 HANDLE FILE
# ==========================
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document.file_name.endswith(".txt"):
        await update.message.reply_text("❌ Vui lòng gửi file định dạng `.txt`.")
        return

    await update.message.reply_text("📥 Đang tải file xuống...")
    file = await context.bot.get_file(document.file_id)
    file_bytes = await file.download_as_bytearray()

    try:
        content = file_bytes.decode("utf-8").strip()
    except Exception:
        await update.message.reply_text("❌ Lỗi đọc file. Vui lòng đảm bảo file là UTF-8.")
        return

    lines = [line.strip() for line in content.splitlines() if "|" in line]
    if not lines:
        await update.message.reply_text("❌ Không tìm thấy dòng hợp lệ trong file.")
        return

    if len(lines) > MAX_LINES:
        await update.message.reply_text(f"⚠️ Giới hạn {MAX_LINES} dòng. Chỉ xử lý {MAX_LINES} dòng đầu tiên.")
        lines = lines[:MAX_LINES]

    await update.message.reply_text(f"🔍 Bắt đầu kiểm tra {len(lines)} tài khoản...")

    results = []
    async with aiohttp.ClientSession() as session:
        for i, line in enumerate(lines, start=1):
            username, password = line.split("|", 1)
            params = {"username": username.strip(), "password": password.strip()}

            try:
                async with session.get(API_URL, params=params, timeout=30) as resp:
                    if resp.status != 200:
                        results.append(f"{i}. {username} ❌ Lỗi HTTP {resp.status}")
                        continue

                    data = await resp.json()
                    if data.get("status") == "success":
                        email = data.get("email", "❌ Không có email")
                        verimail = data.get("verimail", "")
                        results.append(f"{i}. ✅ {username} | {email} | {verimail}")
                    else:
                        results.append(f"{i}. ❌ {username} | {data.get('text', 'Lỗi không xác định')}")

            except asyncio.TimeoutError:
                results.append(f"{i}. {username} ❌ Timeout (quá 30s)")
            except Exception as e:
                results.append(f"{i}. {username} ❌ {type(e).__name__}: {str(e)}")

            await asyncio.sleep(DELAY_BETWEEN_CHECKS)

    # Gửi kết quả
    result_text = "\n".join(results)
    if len(result_text) > 4000:  # Telegram giới hạn tin nhắn 4096 ký tự
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(result_text)
        await update.message.reply_document(InputFile("result.txt"), caption="📄 Kết quả kiểm tra")
    else:
        await update.message.reply_text(f"📊 Kết quả:\n\n{result_text}")

# ==========================
# 🚨 ERROR HANDLER
# ==========================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Lỗi: {context.error}")
    if update and getattr(update, "message", None):
        await update.message.reply_text("❌ Bot gặp lỗi, vui lòng thử lại sau.")

# ==========================
# 🚀 MAIN
# ==========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_error_handler(error_handler)

    logger.info("Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
