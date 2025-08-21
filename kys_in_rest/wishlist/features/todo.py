from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.users.features.check_admin import CheckTgAdmin
from kys_in_rest.wishlist.features.ports.wishlist_repo import WishlistRepo


class ListTodo(TgFeature):
    def __init__(
        self,
        check_tg_admin: CheckTgAdmin,
        bot_msg_repo: BotMsgRepo,
    ):
        self.check_tg_admin = check_tg_admin
        self.bot_msg_repo = bot_msg_repo

    async def do_async(self, msg: InputTgMsg) -> None:
        self.check_tg_admin.do(msg.tg_user_id)

        todos = [
            "Notion: Пивной гайд: https://www.notion.so/e1462a1265784c4dab59a3849a78d537",
            "Читать: Игры, в которые играют люди",
            "Читать: Как варить пиво",
            "Github: potyk-assist: https://github.com/potykion/potyk-assistant/issues",
            "Google Tasks: https://calendar.google.com/calendar/u/0/r/tasks",
        ]
        todo_list_str = "\n".join([f"• {todo}" for todo in todos])
        await self.bot_msg_repo.send_text(f"Чем заняться:\n{todo_list_str}")
