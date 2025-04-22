import itertools

import dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Application,
    CallbackQueryHandler,
)

from kys_in_rest.core.cfg import root_dir
from kys_in_rest.restaurants.features.list_metro import list_metro_items
from kys_in_rest.restaurants.prep.ioc import RestFactory

TG_TOKEN = dotenv.get_key(".env", "TG_TOKEN")

fact = RestFactory(root_dir / "db.sqlite")


async def near_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(update.message.text.split()) == 1:
        metro_items = list_metro_items()

        keyboard = [
            [
                InlineKeyboardButton(metro_str, callback_data=metro_cb)
                for (metro_str, metro_cb) in row
            ]
            for row in itertools.batched(metro_items, 3)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("гдэ??", reply_markup=reply_markup)
        return

    metro = update.message.text.split(None, 1)[1]
    print(metro)

    get_near_restaurants = fact.make_get_near_restaurants()
    near_rests = get_near_restaurants.do(metro)
    await update.message.reply_markdown_v2(near_rests)


async def new_rest_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    add_new_restaurant = fact.make_add_new_restaurant()
    add_new_restaurant.do()


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith("metro_"):
        metro = query.data[6:]  # Убираем префикс "metro_"

        get_near_restaurants = fact.make_get_near_restaurants()
        near_rests = get_near_restaurants.do(metro)

        await query.message.reply_markdown_v2(near_rests)


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            ("near", "Ищет рестики по метро"),
            # todo uncomment when AddNewRestaurant will be implemented
            #   ("new", "Добавить рест"),
        ]
    )


def main():
    app = ApplicationBuilder().token(TG_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("near", near_handler))
    app.add_handler(CommandHandler("new", new_rest_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("run_polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
