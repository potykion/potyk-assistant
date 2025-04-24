import enum
from typing import Callable

import dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Application,
    CallbackQueryHandler,
    MessageHandler,
)

from kys_in_rest.core.cfg import root_dir
from kys_in_rest.core.tg_utils import AskForData, build_keyboard, TgFeature
from kys_in_rest.restaurants.features.add_new import AddNewRestaurant
from kys_in_rest.restaurants.features.list_metro import list_metro_items
from kys_in_rest.restaurants.prep.ioc import RestFactory

TG_TOKEN = dotenv.get_key(".env", "TG_TOKEN")

fact = RestFactory(root_dir / "db.sqlite")


class TgCommand(enum.StrEnum):
    near = enum.auto()
    new = enum.auto()


command_features: dict[TgCommand, Callable[[], TgFeature]] = {
    TgCommand.near: fact.make_get_near_restaurants,
}


async def near_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(update.message.text.split()) == 1:
        metro_items = list_metro_items()
        await update.message.reply_text(
            "гдэ??",
            reply_markup=build_keyboard(metro_items),
        )
        return

    metro = update.message.text.split(None, 1)[1]
    print(metro)

    get_near_restaurants = fact.make_get_near_restaurants()
    near_rests = get_near_restaurants.do(metro)
    await update.message.reply_markdown_v2(near_rests)


async def new_rest_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    add_new_restaurant: AddNewRestaurant = fact.make_add_new_restaurant()

    text = None if text.startswith("/new") else text

    try:
        message = add_new_restaurant.do(text)
    except AskForData as e:
        await update.message.reply_text(
            e.question,
            reply_markup=build_keyboard(e.options) if e.options else None,
        )
    else:
        await update.message.reply_text(message)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith("metro_"):
        metro = query.data[6:]  # Убираем префикс "metro_"

        flow_repo = fact.make_slite_flow_repo()
        flow = flow_repo.get_flow()
        feature = command_features[flow.command]()

        try:
            message = feature.do(metro)
        except AskForData as e:
            await update.message.reply_text(
                e.question,
                reply_markup=build_keyboard(e.options) if e.options else None,
            )
        else:
            await query.message.reply_markdown_v2(message)


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

    app.add_handler(CommandHandler(TgCommand.near, near_handler))
    app.add_handler(CommandHandler(TgCommand.new, new_rest_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    app.add_handler(MessageHandler(None, new_rest_handler))

    print("run_polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
