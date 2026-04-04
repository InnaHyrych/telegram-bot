import logging
import re

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ==================== ТОКЕН ====================
import os

app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

# ==================== СПИСКИ СЛІВ ДЛЯ ВИДАЛЕННЯ ====================

# 1. Криптовалюта: купівля, продаж, обмін
CRYPTO_WORDS = [
    "bitcoin", "btc", "eth", "ethereum", "usdt", "юсдт", "usdc", "bnb", "sol", "xrp",
    "binance", "bybit", "okx", "крипта", "криптовалюта", "биткоин", "криптовалюти", "p2p", "buy", "sell", "trade"
]

# 2. Спам про закриття групи, перехід, фейк-групу
SPAM_PHRASES = [
    "група закривається", "група закривається", "група неактивна", "ця група не дійсна",
    "группа закрывается", "группа неактивна", "перейди по посиланню", "переходь по ссылке",
    "вступай", "присоединяйся", "join", "нова група", "основна група", "основний чат",
    "легкий дохід", "заработок", "заробіток", "easy money", "income"
]

# 3. Порно та еротика
PORNO_WORDS = [
    "порно", "porn", "sex", "секс", "xxx", "18+", "onlyfans", "only fans",
    "еротика", "голая", "голі", "сиськи", "пизда", "хуй", "член", "трах", "ебля",
    "минет", "nude", "naked", "hot girls", "гарячі дівчата", "camgirl", "webcam"
]

# Логування (щоб бачити, що бот видаляє)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def is_admin(update: Update) -> bool:
    """Не чіпаємо повідомлення від адміністраторів і творця групи"""
    try:
        member = await update.message.chat.get_member(update.message.from_user.id)
        return member.status in ["administrator", "creator"]
    except:
        return False


async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    # Якщо автор — адмін, нічого не видаляємо
    if await is_admin(update):
        return

    text = message.text.lower()

    # Видаляємо, якщо знайдено будь-яке заборонене слово
    if (any(word in text for word in CRYPTO_WORDS) or
        any(phrase in text for phrase in SPAM_PHRASES) or
        any(word in text for word in PORNO_WORDS)):

        await message.delete()
        logger.info(f"Видалено спам від {message.from_user.id} | Текст: {message.text[:50]}...")
        return


# ==================== ЗАПУСК БОТА ====================
if __name__ == '__main__':
    print("🚀 Бот для очищення групи від спаму запускається...")
    
    app = ApplicationBuilder().token(TOKEN).build()

    # Обробник всіх текстових повідомлень
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, check_spam))

    print("✅ Бот успішно запущено!")
    print("   Залиш це вікно відкритим.")
    print("   Додай бота в групу як адміністратора з правом «Видаляти повідомлення».")

    # Цей рядок запускає нескінченний цикл бота
    app.run_polling()
