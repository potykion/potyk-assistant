import dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application

from kys_in_rest.near import near

TG_TOKEN = dotenv.get_key(".env", "TG_TOKEN")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def near_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    metro = update.message.text.split(None, 1)[1]
    print(metro)

    near_rests = near(metro)
    await update.message.reply_markdown_v2(near_rests)


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([("near", "Ищет рестики по метро")])


def main():
    app = ApplicationBuilder().token(TG_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("near", near_handler))

    print("run_polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
