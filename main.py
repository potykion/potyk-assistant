import dataclasses
import os
from typing import Type, cast, Any

import dotenv
from telegram import Update, CallbackQuery, Message, User
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
)

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.beer.features.add_new_beer import AddNewBeer
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.core.tg_utils import (
    build_keyboard,
    TgFeature,
    SendTgMessageInterrupt,
)
from kys_in_rest.restaurants.features.add_new import AddNewRestaurant
from kys_in_rest.restaurants.features.find_near_category import (
    FindCategoryRestaurants,
    GetNearRestaurants,
)
from kys_in_rest.tg.entities.flow import TgCommand
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.flow_repo import FlowRepo

dotenv.load_dotenv()
TG_TOKEN = os.environ["TG_TOKEN"]

ioc = make_ioc(str(root_dir / os.environ["DB"]))


@dataclasses.dataclass
class TgCommandSetup:
    command: TgCommand
    feature: Type[TgFeature]

    def make_handler(
        self,
    ) -> Any:
        async def _handler(update: Update, context: Any) -> None:
            await _start_flow_handler(update, self.command)

        return CommandHandler(self.command, _handler)

    def make_feature(self) -> TgFeature:
        return ioc.resolve(self.feature)


tg_commands = [
    TgCommandSetup(TgCommand.category, FindCategoryRestaurants),
    TgCommandSetup(TgCommand.near, GetNearRestaurants),
    TgCommandSetup(TgCommand.new, AddNewRestaurant),
    TgCommandSetup(TgCommand.new_beer, AddNewBeer),
]


def find_command_setup(command: TgCommand) -> TgCommandSetup:
    for setup in tg_commands:
        if setup.command == command:
            return setup
    raise ValueError(f"No {command=} found")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = cast(CallbackQuery, update.callback_query)
    if query:
        await query.answer()
        await _continue_flow_handler(query, InputTgMsg.parse(query))


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _continue_flow_handler(update, InputTgMsg.parse(update))


async def post_init(application: Any) -> None:
    await application.bot.set_my_commands(
        [
            (TgCommand.near, "Ищет рестики по метро"),
            (TgCommand.category, "Ищет рестики по категории"),
            (TgCommand.new, "Добавить рест"),
        ]
    )


async def _start_flow_handler(update: Update, command: TgCommand) -> None:
    user = cast(User, update.effective_user)
    if not user:
        return
    tg_user_id = user.id

    message = cast(Message, update.message)
    if not message:
        return
    text = message.text
    if text and text.startswith(f"/{command}"):
        try:
            text = text.split(None, 1)[1]
        except IndexError:
            text = None

    flow_repo = ioc.resolve(FlowRepo)
    flow = flow_repo.start_or_continue_flow(command, tg_user_id)

    feature: TgFeature = find_command_setup(flow.command).make_feature()

    msg = InputTgMsg(
        text=text,
        tg_user_id=tg_user_id,
    )

    try:
        res = feature.do(msg)
    except SendTgMessageInterrupt as e:
        for err_msg in e.messages:
            await cast(Any, update.message).reply_text(
                err_msg.message,
                reply_markup=build_keyboard(err_msg.options) if err_msg.options else None,
            )
    else:
        await cast(Any, update.message).reply_markdown_v2(res)


async def _continue_flow_handler(
    update_or_query: Update | CallbackQuery,
    msg: InputTgMsg,
) -> None:
    flow_repo = ioc.resolve(FlowRepo)
    flow = flow_repo.get_current_flow(msg.tg_user_id)
    feature = find_command_setup(flow.command).make_feature()

    try:
        message = feature.do(msg)
    except SendTgMessageInterrupt as e:
        for err_msg in e.messages:
            if update_or_query.message:
                await cast(Any, update_or_query.message).reply_text(
                    err_msg.message,
                    reply_markup=(
                        build_keyboard(err_msg.options) if err_msg.options else None
                    ),
                )
    else:
        if update_or_query.message:
            await cast(Any, update_or_query.message).reply_markdown_v2(message)


def main() -> None:
    app = ApplicationBuilder().token(TG_TOKEN).post_init(post_init).build()

    for command in tg_commands:
        app.add_handler(command.make_handler())

    app.add_handler(CallbackQueryHandler(button_callback))

    app.add_handler(MessageHandler(None, message_handler))

    print("run_polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
