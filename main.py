import os
from typing import Callable

import dotenv
from telegram import Update, CallbackQuery
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
from kys_in_rest.restaurants.prep.ioc import RestFactory
from kys_in_rest.tg.entities.flow import TgCommand
from kys_in_rest.tg.features.flow_repo import FlowRepo

dotenv.load_dotenv()
TG_TOKEN = os.environ["TG_TOKEN"]

fact = RestFactory(root_dir / "db.sqlite")


command_features: dict[TgCommand, Callable[[], TgFeature]] = {
    TgCommand.near: fact.make_get_near_restaurants,
    TgCommand.new: fact.make_add_new_restaurant,
}


async def _start_flow_handler(update: Update, command: TgCommand) -> None:
    tg_user_id = update.effective_user.id

    text = update.message.text
    if text.startswith(f"/{command}"):
        try:
            text = text.split(None, 1)[1]
        except IndexError:
            text = None

    flow_repo: FlowRepo = fact.make_flow_repo()
    flow = flow_repo.start_or_continue_flow(command, tg_user_id)
    feature = command_features[flow.command]()

    try:
        message = feature.do(text, tg_user_id)
    except AskForData as e:
        await update.message.reply_text(
            e.question,
            reply_markup=build_keyboard(e.options) if e.options else None,
        )
    else:
        await update.message.reply_markdown_v2(message)


async def _continue_flow_handler(
    update_or_query: Update | CallbackQuery,
    text,
):
    if isinstance(update_or_query, CallbackQuery):
        tg_user_id = update_or_query.from_user.id
    else:
        tg_user_id = update_or_query.effective_user.id

    flow_repo = fact.make_flow_repo()
    flow = flow_repo.get_current_flow(tg_user_id)
    feature = command_features[flow.command]()

    try:
        message = feature.do(text, tg_user_id)
    except AskForData as e:
        await update_or_query.message.reply_text(
            e.question,
            reply_markup=build_keyboard(e.options) if e.options else None,
        )
    else:
        await update_or_query.message.reply_markdown_v2(message)


async def near_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _start_flow_handler(update, TgCommand.near)


async def new_rest_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _start_flow_handler(update, TgCommand.new)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await _continue_flow_handler(query, query.data)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _continue_flow_handler(update, update.message.text)


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            (TgCommand.near, "Ищет рестики по метро"),
            (TgCommand.new, "Добавить рест"),
        ]
    )


def main():
    app = ApplicationBuilder().token(TG_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler(TgCommand.near, near_handler))
    app.add_handler(CommandHandler(TgCommand.new, new_rest_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    app.add_handler(MessageHandler(None, message_handler))

    print("run_polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
