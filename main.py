import os
import re
from typing import cast, Any

import dotenv
from telegram import Update, CallbackQuery, Message, User
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    CommandHandler,
)

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.beer.features.add_new_beer import AddNewBeer
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.core.tg_utils import (
    build_keyboard,
    TgFeature,
    SendTgMessageInterrupt,
)
from kys_in_rest.health.features.add_weight import AddOrShowWeight
from kys_in_rest.money.features.add_goal import AddMoneyGoal
from kys_in_rest.money.features.add_spending import AddSpending
from kys_in_rest.money.features.goal_budget import PlanGoalBudgets
from kys_in_rest.money.features.sync_zen_money import SyncZenMoney
from kys_in_rest.music.features.download import DownloadMusic
from kys_in_rest.restaurants.features.add_new import AddNewRestaurant
from kys_in_rest.restaurants.features.find_near_category import (
    FindCategoryRestaurants,
    GetNearRestaurants,
)
from kys_in_rest.tg.entities.command import TgCommandSetup
from kys_in_rest.tg.entities.flow import TgCommand
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.tg.features.flow_repo import FlowRepo
from kys_in_rest.tg.features.help import Help
from kys_in_rest.tg.features.id import ShowTgId
from kys_in_rest.tg.features.my_tg_channels import ListMyTgChannels
from kys_in_rest.tg.infra.bot_msg_repo import TgUpdateBotMsgRepo
from kys_in_rest.wishlist.features.wishlist import Wishlist

dotenv.load_dotenv(root_dir / ".env")
TG_TOKEN = os.environ["TG_TOKEN"]


ioc = make_ioc(
    db_path=str(root_dir / os.environ["DB"]),
    tg_admins=list(map(int, os.environ["TG_ADMINS"].split(","))),
    yandex_music_token=os.environ["YANDEX_MUSIC_TOKEN"],
    zen_money_token=os.environ["ZEN_MONEY_TOKEN"],
    # fmt: off
    tg_commands=[
        TgCommandSetup(TgCommand.wishlist, "Вишлист (показать/добавить предмет)", Wishlist),
        TgCommandSetup(TgCommand.weight_ru, "Добавить вес", AddOrShowWeight),
        TgCommandSetup(TgCommand.weight, "Добавить вес", AddOrShowWeight),
        TgCommandSetup(TgCommand.start, "Справка по всем командам", Help),
        TgCommandSetup(TgCommand.my_tg_channels, "Мои тг каналы", ListMyTgChannels),
        TgCommandSetup(TgCommand.mu, "Скачать mp3 (ЯМузыка)", DownloadMusic),
        TgCommandSetup(TgCommand.id, "Узнать свой Телеграм ID", ShowTgId),
        TgCommandSetup(TgCommand.help, "Справка по всем командам", Help),
        # TgCommandSetup(TgCommand.zen_money_sync, "Синхрон Дзен-мани", SyncZenMoney),
        # TgCommandSetup(TgCommand.w, "Добавить вес", AddOrShowWeight),
        # TgCommandSetup(TgCommand.spend_ru, "Добавить расход", AddSpending),
        # TgCommandSetup(TgCommand.spend, "Добавить расход", AddSpending),
        # TgCommandSetup(TgCommand.rest_metro, "Найти ресты у метро", GetNearRestaurants),
        # TgCommandSetup(TgCommand.rest_cat, "Найти ресты по категории", FindCategoryRestaurants),
        # TgCommandSetup(TgCommand.new_beer, "Добавить пивко", AddNewBeer),
        # TgCommandSetup(TgCommand.new, "Добавить рест", AddNewRestaurant),
        # TgCommandSetup(TgCommand.mon_goal_budget, "Планирование бюджетов", PlanGoalBudgets),
        # TgCommandSetup(TgCommand.mon_goal, "Добавить цель", AddMoneyGoal),
        # TgCommandSetup(TgCommand.mon, "Добавить расход / вывод трат", AddSpending),
        # TgCommandSetup(TgCommand.download, "Скачать mp3 (ЯМузыка)", DownloadMusic),
    ],
    # fmt: on
)


def find_command_setup(command: TgCommand | str) -> TgCommandSetup:
    for setup in cast(list[TgCommandSetup], ioc.tg_commands):
        if setup.command == command:
            return setup
    raise ValueError(f"No {command=} found")


def command_parser(text: str) -> tuple[TgCommand | None, str | None]:
    """
    Парсит команду из текста и возвращает (команда, аргументы).
    Поддерживает case-insensitive поиск команд.
    
    Args:
        text: Текст сообщения для парсинга
        
    Returns:
        Кортеж (команда, аргументы) или (None, None) если команда не найдена
        
    Examples:
    >>> from kys_in_rest.tg.entities.flow import TgCommand
    >>> command_parser("/вес 75.5")
    (<TgCommand.weight_ru: 'вес'>, '75.5')
    >>> command_parser("/Вес 80")
    (<TgCommand.weight_ru: 'вес'>, '80')
    >>> command_parser("вес 70")
    (<TgCommand.weight_ru: 'вес'>, '70')
    >>> command_parser("Вес 70")
    (<TgCommand.weight_ru: 'вес'>, '70')
    >>> command_parser("/weight 65")
    (<TgCommand.weight: 'weight'>, '65')
    >>> command_parser("/вес")
    (<TgCommand.weight_ru: 'вес'>, None)
    >>> command_parser("/unknown")
    (None, None)
    >>> command_parser("")
    (None, None)
    >>> command_parser("/вес   75.5  кг")
    (<TgCommand.weight_ru: 'вес'>, '75.5  кг')
    """
    if not text:
        return None, None
    
    # Разбиваем на команду и аргументы
    parts = text.strip().split(None, 1)
    command_str = parts[0]
    args = parts[1] if len(parts) > 1 else None
    
    # Убираем слэш если есть
    if command_str.startswith("/"):
        command_str = command_str[1:]
    
    # Поиск команды (case-insensitive)
    command_str_lower = command_str.lower()
    
    # Сначала пробуем точное совпадение
    try:
        command = TgCommand(command_str)
        return command, args
    except ValueError:
        pass
    
    # Затем пробуем case-insensitive поиск
    for command in TgCommand:
        if command.value.lower() == command_str_lower:
            return command, args
    
    return None, None


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = cast(CallbackQuery, update.callback_query)
    if query:
        await query.answer()
        await _continue_flow_handler(query, InputTgMsg.parse(query))


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = InputTgMsg.parse(update)

    ioc.register(BotMsgRepo, TgUpdateBotMsgRepo(cast(Message, update.message)))

    command, args = command_parser(msg.text or "")

    if command:
        await _start_flow_handler(update, command, args)
    else:
        await _continue_flow_handler(update, msg)


async def _start_flow_handler(update: Update, command: TgCommand, args: str | None = None) -> None:
    user = cast(User, update.effective_user)
    if not user:
        return
    tg_user_id = user.id

    message = cast(Message, update.message)
    if not message:
        return

    flow_repo = ioc.resolve(FlowRepo)
    flow = flow_repo.start_or_continue_flow(command, tg_user_id)

    ioc.register(BotMsgRepo, TgUpdateBotMsgRepo(message))

    feature = cast(TgFeature, ioc[find_command_setup(flow.command).feature])

    msg = InputTgMsg(
        text=args,
        tg_user_id=tg_user_id,
    )

    try:
        try:
            await feature.do_async(msg)
            result_msg = None
        except NotImplementedError:
            result_msg = feature.do(msg)
    except SendTgMessageInterrupt as e:
        for err_msg in e.messages:
            await cast(Any, update.message).reply_text(
                err_msg.message,
                reply_markup=(
                    build_keyboard(err_msg.options) if err_msg.options else None
                ),
            )
        return

    if isinstance(result_msg, tuple):
        reply, ops = result_msg

        if ops["parse_mode"] is None:
            await cast(Message, update.message).reply_text(reply)
        elif ops["parse_mode"] == "html":
            await cast(Message, update.message).reply_html(reply)
        else:
            await cast(Any, update.message).reply_markdown_v2(reply)

    elif isinstance(result_msg, str) and result_msg:
        reply = result_msg
        await cast(Any, update.message).reply_markdown_v2(reply)


async def _continue_flow_handler(
    update_or_query: Update | CallbackQuery,
    msg: InputTgMsg,
) -> None:
    flow_repo = ioc.resolve(FlowRepo)
    flow = flow_repo.get_current_flow(msg.tg_user_id)
    feature = cast(TgFeature, ioc[find_command_setup(flow.command).feature])

    try:
        try:
            await feature.do_async(msg)
            message = None
        except NotImplementedError:
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
        if update_or_query.message and message:
            await cast(Any, update_or_query.message).reply_markdown_v2(message)


async def post_init(application: Any) -> None:
    await application.bot.set_my_commands(
        [(setup.command, setup.desc) for setup in filter_en_commands()]
    )


def main() -> None:
    app = ApplicationBuilder().token(TG_TOKEN).post_init(post_init).build()

    en_commands = filter_en_commands()
    for setup in en_commands:
        app.add_handler(CommandHandler(setup.command, make_handler(setup)))

    app.add_handler(CallbackQueryHandler(button_callback))

    app.add_handler(MessageHandler(None, message_handler))

    print("run_polling...")
    app.run_polling()


def filter_en_commands() -> list[TgCommandSetup]:
    en_commands = [
        c
        for c in cast(list[TgCommandSetup], ioc.tg_commands)
        if re.match(r"^[\da-z_]{1,32}$", c.command)
    ]
    return en_commands


def make_handler(setup: TgCommandSetup) -> Any:
    async def _handler(update: Update, context: Any) -> None:
        # Извлекаем аргументы из текста сообщения
        message = cast(Message, update.message)
        text = message.text if message else ""
        _, args = command_parser(text)
        await _start_flow_handler(update, setup.command, args)

    return _handler


if __name__ == "__main__":
    main()
