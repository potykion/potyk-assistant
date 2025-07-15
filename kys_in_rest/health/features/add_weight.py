import io

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from kys_in_rest.core.tg_utils import (
    TgFeature,
    tg_escape,
)
from kys_in_rest.health.entities.weight import WeightEntry
from kys_in_rest.health.features.weight_repo import WeightRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.users.features.check_admin import CheckTgAdmin


class AddOrShowWeight(TgFeature):
    def __init__(
        self,
        weight_repo: WeightRepo,
        check_tg_admin: CheckTgAdmin,
        bot_msg_repo: BotMsgRepo,
    ):
        self.weight_repo = weight_repo
        self.check_tg_admin = check_tg_admin
        self.bot_msg_repo = bot_msg_repo

    def _create_weight_chart(self, entries: list[WeightEntry]) -> bytes:
        """Создает график веса и возвращает его как байты"""
        if not entries:
            return None
            
        # Сортируем записи по дате
        entries.sort(key=lambda x: x.date)
        
        dates = [entry.date for entry in entries]
        weights = [entry.weight for entry in entries]
        
        # Создаем график
        plt.figure(figsize=(10, 6))
        plt.plot(dates, weights, 'b-o', linewidth=2, markersize=6)
        
        # Настройка осей
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Вес (кг)', fontsize=12)
        plt.title('График изменения веса', fontsize=14, fontweight='bold')
        
        # Форматирование оси X
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        # Уменьшаем количество меток на оси X - максимум 4-5 меток
        interval = max(1, len(dates) // 3)
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        plt.xticks(rotation=45)
        
        # Добавляем сетку
        plt.grid(True, alpha=0.3)
        
        # Добавляем последний вес как аннотацию
        if entries:
            last_entry = entries[-1]
            plt.annotate(
                f'{last_entry.weight} кг',
                xy=(last_entry.date, last_entry.weight),
                xytext=(10, 10),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
            )
        
        # Настройка отступов
        plt.tight_layout()
        
        # Сохраняем в байты
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer.getvalue()

    async def _send_weight_chart(self, entries: list[WeightEntry], is_update: bool = False) -> None:
        """Отправляет график веса с соответствующей подписью"""
        if not entries:
            await self.bot_msg_repo.send_text(tg_escape("Нет записей о весе. Добавь через /weight {вес}"))
            return

        chart_bytes = self._create_weight_chart(entries)
        if not chart_bytes:
            await self.bot_msg_repo.send_text(tg_escape("Ошибка при создании графика"))
            return

        last_entry = entries[-1]
        if is_update:
            caption = f"Обновленный график веса\nНовый вес: {last_entry.weight} кг от {last_entry.date.strftime('%d.%m.%Y')}"
        else:
            caption = f"График веса\nПоследний вес: {last_entry.weight} кг от {last_entry.date.strftime('%d.%m.%Y')}"
        
        await self.bot_msg_repo.send_photo(chart_bytes, caption)

    async def do_async(self, msg: InputTgMsg) -> None:
        self.check_tg_admin.do(msg.tg_user_id)

        if msg.text:
            # Добавляем новый вес
            weight = float(msg.text)
            self.weight_repo.add_weight_entry(WeightEntry(weight=weight))
            await self.bot_msg_repo.send_text("Записал 👌")
            
            # Показываем обновленный график
            entries = self.weight_repo.list_weight_entries()
            await self._send_weight_chart(entries, is_update=True)
            return

        # Показываем текущий график
        entries = self.weight_repo.list_weight_entries()
        await self._send_weight_chart(entries, is_update=False)
