from datetime import datetime, timedelta

from tinkoff.invest import Client, CandleInterval

from kys_in_rest.money.features.repos.tinkoff_candles_repo import (
    Candle,
    TinkoffCandlesRepo,
)


class TinkoffInvestCandlesRepo(TinkoffCandlesRepo):
    """Реализация репозитория для получения свечей через Tinkoff Investments API"""

    def __init__(self, token: str):
        self.token = token

    def get_monthly_candles(self, ticker: str, months: int = 36) -> list[Candle]:
        """
        Получает месячные свечи за указанное количество месяцев
        
        Args:
            ticker: Тикер акции (например, 'NLMK')
            months: Количество месяцев (по умолчанию 36)
            
        Returns:
            Список свечей, отсортированный по времени (от старых к новым)
        """
        with Client(token=self.token) as client:
            # Получаем инструмент по тикеру
            instruments_response = client.instruments.find_instrument(query=ticker)
            
            # Ищем акцию на Московской бирже
            instrument = None
            if hasattr(instruments_response, 'instruments'):
                for inst in instruments_response.instruments:
                    if hasattr(inst, 'ticker') and hasattr(inst, 'exchange'):
                        if inst.ticker == ticker.upper() and inst.exchange == "MOEX":
                            instrument = inst
                            break
            
            if not instrument or not hasattr(instrument, 'figi'):
                raise ValueError(f"Инструмент {ticker} не найден на Московской бирже")
            
            # Получаем figi инструмента
            figi = instrument.figi
            
            # Вычисляем даты начала и конца
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=months * 31)  # Примерно months месяцев
            
            # Получаем свечи
            candles_response = client.market_data.get_candles(
                figi=figi,
                from_=start_date,
                to=end_date,
                interval=CandleInterval.CANDLE_INTERVAL_MONTH,
            )
            
            # Преобразуем в наши Candle объекты
            candles = []
            if hasattr(candles_response, 'candles'):
                for candle in candles_response.candles:
                    if (hasattr(candle, 'open') and candle.open and 
                        hasattr(candle, 'close') and candle.close and
                        hasattr(candle, 'high') and candle.high and
                        hasattr(candle, 'low') and candle.low):
                        # Преобразуем Quotation в float
                        open_price = float(candle.open.units) + float(candle.open.nano) / 1e9
                        close_price = float(candle.close.units) + float(candle.close.nano) / 1e9
                        high_price = float(candle.high.units) + float(candle.high.nano) / 1e9
                        low_price = float(candle.low.units) + float(candle.low.nano) / 1e9
                        
                        candles.append(
                            Candle(
                                open=open_price,
                                close=close_price,
                                high=high_price,
                                low=low_price,
                                time=candle.time,
                                volume=candle.volume if hasattr(candle, 'volume') else 0,
                            )
                        )
            
            # Сортируем по времени (от старых к новым)
            candles.sort(key=lambda c: c.time)
            
            return candles

