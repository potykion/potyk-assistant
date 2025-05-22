import dataclasses
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
from kys_in_rest.core.tg_utils import (
    build_keyboard,
    TgFeature,
    SendTgMessageInterrupt,
)
from kys_in_rest.applications.ioc import MainFactory
from kys_in_rest.tg.entities.flow import TgCommand
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.flow_repo import FlowRepo

dotenv.load_dotenv()
TG_TOKEN = os.environ["TG_TOKEN"]

fact = MainFactory(root_dir / os.environ["DB"])


@dataclasses.dataclass
class TgCommandSetup:
    command: TgCommand
    feature: Callable[[], TgFeature]

    def make_handler(self):
        async def _handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await _start_flow_handler(update, self.command)

        return CommandHandler(self.command, _handler)


tg_commands = [
    TgCommandSetup(TgCommand.category, fact.make_find_category_restaurants),
    TgCommandSetup(TgCommand.near, fact.make_get_near_restaurants),
    TgCommandSetup(TgCommand.new, fact.make_add_new_restaurant),
    TgCommandSetup(TgCommand.new_beer, fact.make_add_new_beer),
]


def find_command_setup(command) -> TgCommandSetup:
    for setup in tg_commands:
        if setup.command == command:
            return setup
    raise ValueError(f"No {command=} found")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await _continue_flow_handler(query, InputTgMsg.parse(query))


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _continue_flow_handler(update, InputTgMsg.parse(update))


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            (TgCommand.near, "Ищет рестики по метро"),
            (TgCommand.category, "Ищет рестики по категории"),
            (TgCommand.new, "Добавить рест"),
        ]
    )


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

    feature: TgFeature = find_command_setup(flow.command).feature()

    msg = InputTgMsg(
        text=text,
        tg_user_id=tg_user_id,
    )

    try:
        message = feature.do(msg)
    except SendTgMessageInterrupt as e:
        for msg in e.messages:
            await update.message.reply_text(
                msg.message,
                reply_markup=build_keyboard(msg.options) if msg.options else None,
            )
    else:
        await update.message.reply_markdown_v2(message)


async def _continue_flow_handler(
    update_or_query: Update | CallbackQuery,
    msg: InputTgMsg,
):

    flow_repo = fact.make_flow_repo()
    flow = flow_repo.get_current_flow(msg.tg_user_id)
    feature = find_command_setup(flow.command).feature()

    try:
        message = feature.do(msg)
    except SendTgMessageInterrupt as e:
        for msg in e.messages:
            await update_or_query.message.reply_text(
                msg.message,
                reply_markup=build_keyboard(msg.options) if msg.options else None,
            )
    else:
        await update_or_query.message.reply_markdown_v2(message)


def main():
    app = ApplicationBuilder().token(TG_TOKEN).post_init(post_init).build()

    for command in tg_commands:
        app.add_handler(command.make_handler())

    app.add_handler(CallbackQueryHandler(button_callback))

    app.add_handler(MessageHandler(None, message_handler))

    print("run_polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
