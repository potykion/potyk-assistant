from datetime import datetime, timedelta, timezone
from typing import Any

from tinkoff.invest import CandleInterval, Client, InstrumentIdType

from kys_in_rest.money.features.repos.tinkoff_candles_repo import Candle, TinkoffCandlesRepo


class TinkoffInvestCandlesRepo(TinkoffCandlesRepo):
    """Реализация репозитория для получения свечей через Tinkoff Investments API"""

    def __init__(self, token: str):
        self.token = token

    def get_monthly_candles(self, ticker: str, months: int = 36) -> list[Candle]:
        with Client(token=self.token) as client:
            figi = self._resolve_figi(client, ticker)
            end_date = datetime.utcnow().replace(tzinfo=timezone.utc)
            start_date = end_date - timedelta(days=months * 31)
            return self._fetch_candles(
                client,
                figi=figi,
                from_=start_date,
                to=end_date,
                interval=CandleInterval.CANDLE_INTERVAL_MONTH,
            )

    def get_weekly_candles(self, ticker: str, weeks: int = 156) -> list[Candle]:
        with Client(token=self.token) as client:
            figi = self._resolve_figi(client, ticker)
            end_date = datetime.utcnow().replace(tzinfo=timezone.utc)
            start_date = end_date - timedelta(weeks=weeks)
            return self._fetch_candles(
                client,
                figi=figi,
                from_=start_date,
                to=end_date,
                interval=CandleInterval.CANDLE_INTERVAL_WEEK,
            )

    def _resolve_figi(self, client: Any, ticker: str) -> str:
        try:
            share_response = client.instruments.share_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
                class_code="TQBR",
                id=ticker.upper(),
            )
            figi = getattr(share_response.instrument, "figi", None)
            if not figi:
                raise ValueError
            return str(figi)
        except Exception:
            instruments_response = client.instruments.find_instrument(query=ticker)
            instrument = None
            if hasattr(instruments_response, "instruments"):
                for inst in instruments_response.instruments:
                    if hasattr(inst, "ticker") and hasattr(inst, "exchange"):
                        if inst.ticker == ticker.upper() and inst.exchange == "MOEX":
                            instrument = inst
                            break

            figi = getattr(instrument, "figi", None) if instrument else None
            if not figi:
                raise ValueError(f"Инструмент {ticker} не найден на Московской бирже")

            return str(figi)

    def _fetch_candles(
        self,
        client: Any,
        *,
        figi: str,
        from_: datetime,
        to: datetime,
        interval: CandleInterval,
    ) -> list[Candle]:
        candles_response = client.market_data.get_candles(
            figi=figi,
            from_=from_,
            to=to,
            interval=interval,
        )

        candles: list[Candle] = []
        response_candles = getattr(candles_response, "candles", [])
        for candle in response_candles:
            if not (candle.open and candle.close and candle.high and candle.low):
                continue

            candles.append(
                Candle(
                    open=self._quotation_to_float(candle.open),
                    close=self._quotation_to_float(candle.close),
                    high=self._quotation_to_float(candle.high),
                    low=self._quotation_to_float(candle.low),
                    time=candle.time,
                    volume=getattr(candle, "volume", 0),
                )
            )

        candles.sort(key=lambda c: c.time)
        return candles

    def get_current_price(self, ticker: str) -> float:
        """Получает текущую цену инструмента"""
        with Client(token=self.token) as client:
            figi = self._resolve_figi(client, ticker)
            last_prices_response = client.market_data.get_last_prices(figi=[figi])
            if not last_prices_response.last_prices:
                raise ValueError(f"Не удалось получить текущую цену для {ticker}")
            last_price = last_prices_response.last_prices[0]
            if not last_price.price:
                raise ValueError(f"Цена не найдена для {ticker}")
            return self._quotation_to_float(last_price.price)

    @staticmethod
    def _quotation_to_float(quotation: Any) -> float:
        return float(quotation.units) + float(quotation.nano) / 1e9

