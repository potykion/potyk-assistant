import dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application, CallbackQueryHandler

from kys_in_rest.near import near, metro_colors

TG_TOKEN = dotenv.get_key(".env", "TG_TOKEN")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def near_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(update.message.text.split()) == 1:
        # Команда вызвана без параметров
        keyboard = []
        row = []
        for i, (metro, color) in enumerate(sorted(metro_colors.items(), key=lambda item: item[1])):
            row.append(InlineKeyboardButton(f"{color} {metro}", callback_data=f"metro_{metro}"))
            if (i + 1) % 3 == 0:  # По 3 кнопки в ряду
                keyboard.append(row)
                row = []
        if row:  # Добавляем оставшиеся кнопки
            keyboard.append(row)
            
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Где?", reply_markup=reply_markup)
        return
        
    metro = update.message.text.split(None, 1)[1]
    print(metro)

    near_rests = near(metro)
    await update.message.reply_markdown_v2(near_rests)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("metro_"):
        metro = query.data[6:]  # Убираем префикс "metro_"
        near_rests = near(metro)
        await query.message.reply_markdown_v2(near_rests)


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([("near", "Ищет рестики по метро")])


def main():
    app = ApplicationBuilder().token(TG_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("near", near_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("run_polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
