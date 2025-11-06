import io

from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font

from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.money.features.repos.tinkoff_candles_repo import TinkoffCandlesRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.users.features.check_admin import CheckTgAdmin


class LoadCandlesTgFeature(TgFeature):
    def __init__(
        self,
        bot_msg_repo: BotMsgRepo,
        check_tg_admin: CheckTgAdmin,
        candles_repo: TinkoffCandlesRepo,
    ):
        self.bot_msg_repo = bot_msg_repo
        self.check_tg_admin = check_tg_admin
        self.candles_repo = candles_repo

    async def do_async(self, msg: InputTgMsg) -> None:
        self.check_tg_admin.do(msg.tg_user_id)

        # Получаем тикер из сообщения
        ticker = (msg.text or "").strip().upper()
        if not ticker:
            await self.bot_msg_repo.send_text("Укажи тикер акции (например: NLMK)")
            return

        try:
            await self.bot_msg_repo.send_text(f"Загружаю свечи для {ticker}...")
            
            # Получаем свечи
            candles = self.candles_repo.get_monthly_candles(ticker, months=36)
            
            if not candles:
                await self.bot_msg_repo.send_text(f"Не удалось получить свечи для {ticker}")
                return

            # Создаем Excel файл
            excel_bytes = self._create_excel(candles, ticker)
            
            # Вычисляем статистику
            stats = self._calculate_statistics(candles)
            
            # Отправляем файл
            filename = f"{ticker}_candles_36m.xlsx"
            await self.bot_msg_repo.send_document(
                document=excel_bytes,
                filename=filename,
                caption=f"Месячные свечи {ticker} за 36 месяцев",
            )
            
            # Отправляем статистику
            stats_text = self._format_statistics(stats, ticker)
            await self.bot_msg_repo.send_text(stats_text)
            
        except ValueError as e:
            await self.bot_msg_repo.send_text(f"Ошибка: {str(e)}")
        except Exception as e:
            await self.bot_msg_repo.send_text(f"Произошла ошибка: {str(e)}")

    def _create_excel(self, candles: list, ticker: str) -> bytes:
        """Создает Excel файл со свечами"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Свечи"
        
        # Заголовки
        ws["A1"] = "Месяц Год"
        ws["B1"] = "Изменение (%)"
        
        # Стили для заголовков
        header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        header_font = Font(bold=True)
        ws["A1"].fill = header_fill
        ws["A1"].font = header_font
        ws["B1"].fill = header_fill
        ws["B1"].font = header_font
        
        # Заполняем данные
        green_fill = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")
        red_fill = PatternFill(start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")
        
        for idx, candle in enumerate(candles, start=2):
            # Месяц и год
            month_year = candle.time.strftime("%m.%Y")
            ws[f"A{idx}"] = month_year
            
            # Процент изменения
            change_percent = ((candle.close - candle.open) / candle.open) * 100
            ws[f"B{idx}"] = round(change_percent, 2)
            
            # Цвет в зависимости от направления
            if change_percent >= 0:
                ws[f"B{idx}"].fill = green_fill
            else:
                ws[f"B{idx}"].fill = red_fill
        
        # Автоподбор ширины колонок
        ws.column_dimensions["A"].width = 15
        ws.column_dimensions["B"].width = 18
        
        # Сохраняем в байты
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        return excel_buffer.getvalue()

    def _calculate_statistics(self, candles: list) -> dict:
        """Вычисляет статистику по свечам"""
        changes = []
        for candle in candles:
            change_percent = ((candle.close - candle.open) / candle.open) * 100
            changes.append(change_percent)
        
        # Разделяем на рост и падение
        growths = [c for c in changes if c >= 0]
        falls = [c for c in changes if c < 0]
        
        stats = {
            "total": len(changes),
            "growth_count": len(growths),
            "fall_count": len(falls),
        }
        
        if falls:
            stats["min_fall"] = round(min(falls), 2)
            stats["max_fall"] = round(max(falls), 2)
            stats["avg_fall"] = round(sum(falls) / len(falls), 2)
        else:
            stats["min_fall"] = None
            stats["max_fall"] = None
            stats["avg_fall"] = None
        
        if growths:
            stats["min_growth"] = round(min(growths), 2)
            stats["max_growth"] = round(max(growths), 2)
            stats["avg_growth"] = round(sum(growths) / len(growths), 2)
        else:
            stats["min_growth"] = None
            stats["max_growth"] = None
            stats["avg_growth"] = None
        
        return stats

    def _format_statistics(self, stats: dict, ticker: str) -> str:
        """Форматирует статистику для отправки"""
        lines = [f"📊 Статистика по {ticker}:"]
        lines.append("")
        
        # Падения
        if stats["min_fall"] is not None:
            lines.append("🔴 Падения:")
            lines.append(f"  Мин падение: {stats['min_fall']}%")
            lines.append(f"  Макс падение: {stats['max_fall']}%")
            lines.append(f"  Среднее падение: {stats['avg_fall']}%")
        else:
            lines.append("🔴 Падения: нет")
        
        lines.append("")
        
        # Рост
        if stats["min_growth"] is not None:
            lines.append("🟢 Рост:")
            lines.append(f"  Мин рост: {stats['min_growth']}%")
            lines.append(f"  Макс рост: {stats['max_growth']}%")
            lines.append(f"  Средний рост: {stats['avg_growth']}%")
        else:
            lines.append("🟢 Рост: нет")
        
        lines.append("")
        
        # Соотношение
        lines.append(f"📈 Соотношение:")
        lines.append(f"  Рост: {stats['growth_count']} мес")
        lines.append(f"  Падение: {stats['fall_count']} мес")
        lines.append(f"  Всего: {stats['total']} мес")
        
        return "\n".join(lines)
