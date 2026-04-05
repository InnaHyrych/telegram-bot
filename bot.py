import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

CRYPTO_WORDS = [
    "bitcoin", "btc", "eth", "ethereum", "usdt", "юсдт", "usdc", "bnb", "sol", "xrp",
    "binance", "bybit", "okx", "крипта", "криптовалюта", "биткоин", "криптовалюти", "p2p", "buy", "sell", "trade"
]

SPAM_PHRASES = [
    "група закривається", "група закривається", "група неактивна", "ця група не дійсна",
    "группа закрывается", "группа неактивна", "перейди по посиланню", "переходь по ссылке",
    "вступай", "присоединяйся", "join", "нова група", "основна група", "основний чат",
    "легкий дохід", "заработок", "заробіток", "easy money", "income"
]

ADULT_SPAM = [
    "порно", "porn", "sex", "секс", "xxx", "18+", "onlyfans", "only fans",
    "еротика", "голая", "голі", "сиськи", "пизда", "хуй", "член", "трах", "ебля",
    "минет", "nude", "naked", "hot girls", "гарячі дівчата", "camgirl", "webcam"
]

LINK_PATTERNS = [
    r"http[s]?://",
    r"t\.me/",
    r"@\w+"
]


async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message:
        return

    # Ігнор адмінів
    member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=message.from_user.id
    )

    if member.status in ["administrator", "creator"]:
        return

    text = ""

    if message.text:
        text = message.text.lower()
    elif message.caption:
        text = message.caption.lower()

    # Кнопки
    if message.reply_markup:
        await message.delete()
        return

    # Лінки
    for pattern in LINK_PATTERNS:
        if re.search(pattern, text):
            await message.delete()
            return

    # Крипта + торгівля
    if any(c in text for c in CRYPTO_WORDS) and any(t in text for t in TRADE_WORDS):
        await message.delete()
        return

    # Adult
    if any(a in text for a in ADULT_SPAM):
        await message.delete()
        return


app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

app.add_handler(MessageHandler(filters.ALL, check_message))

app.run_polling()
