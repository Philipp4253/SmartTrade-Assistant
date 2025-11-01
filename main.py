import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from utils.ai_client import ask_openrouter

# --- Логирование ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- Создаём широкие кнопки (ReplyKeyboard) ---
def get_main_menu():
    row1 = [KeyboardButton("💡 Совет"), KeyboardButton("📊 Анализ")]
    row2 = [KeyboardButton("🧭 Стратегия"), KeyboardButton("🔥 Мотивация")]
    return ReplyKeyboardMarkup([row1, row2], resize_keyboard=True)

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
    "Привет, трейдер!\n"
    "Я SmartTrade Assistant — твой AI-помощник по рынку! 📊\n"
    "Я помогу тебе:\n"
    "1️⃣ Разобраться с рыночными новостями;\n"
    "2️⃣ Получить краткие советы по трейдингу;\n"
    "3️⃣ Составить стратегию торговли;\n"
    "4️⃣ Найти мотивацию и поддержку после сложных сделок 💪\n"
    "Нажми кнопку 👇 чтобы начать!"
    )
    await update.message.reply_text(text, reply_markup=get_main_menu())

# --- Команда /advice ---
async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = "Дай краткий совет по трейдингу, связанный с управлением рисками, дисциплиной или анализом рынка."
    resp = await ask_openrouter(prompt)
    await update.message.reply_text(resp, reply_markup=get_main_menu())

# --- Команда /analyze ---
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Укажи текст для анализа: /analyze <текст>", reply_markup=get_main_menu())
        return

    prompt = f"Проанализируй следующую ситуацию и сделай вывод: {text}"
    resp = await ask_openrouter(prompt)
    await update.message.reply_text(resp, reply_markup=get_main_menu())

# --- Команда /strategy ---
async def strategy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = "Составь простой шаблон торговой стратегии для начинающего трейдера с пояснениями."
    resp = await ask_openrouter(prompt)
    await update.message.reply_text(resp, reply_markup=get_main_menu())

# --- Команда /motivation ---
async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = "Дай короткое мотивирующее сообщение для трейдера, чтобы он не сдался после серии убыточных сделок."
    resp = await ask_openrouter(prompt)
    await update.message.reply_text(resp, reply_markup=get_main_menu())

# --- Обработка нажатий на кнопки (они приходят как текст) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if user_message == "💡 Совет":
        await advice(update, context)
    elif user_message == "📊 Анализ":
        await update.message.reply_text("Отправь текст или новость для анализа:", reply_markup=get_main_menu())
    elif user_message == "🧭 Стратегия":
        await strategy(update, context)
    elif user_message == "🔥 Мотивация":
        await motivation(update, context)
    else:
        # Пользователь ввёл что-то сам — анализируем
        prompt = f"Пользователь спрашивает: {user_message}"
        resp = await ask_openrouter(prompt)
        await update.message.reply_text(resp, reply_markup=get_main_menu())

# --- main ---
def main():
    logger.info("🚀 Запуск SmartTrade Assistant...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("advice", advice))
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(CommandHandler("strategy", strategy))
    app.add_handler(CommandHandler("motivation", motivation))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Бот запущен и ожидает сообщений...")
    app.run_polling()

if __name__ == "__main__":
    main()
