import abc
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candle:
    """Месячная свеча"""
    open: float  # Цена открытия
    close: float  # Цена закрытия
    high: float  # Максимальная цена
    low: float  # Минимальная цена
    time: datetime  # Время свечи
    volume: int  # Объем


class TinkoffCandlesRepo(abc.ABC):
    """Репозиторий для получения свечей с Tinkoff Investments API"""
    
    @abc.abstractmethod
    def get_monthly_candles(self, ticker: str, months: int = 36) -> list[Candle]:
        """
        Получает месячные свечи за указанное количество месяцев
        
        Args:
            ticker: Тикер акции (например, 'NLMK')
            months: Количество месяцев (по умолчанию 36)
            
        Returns:
            Список свечей, отсортированный по времени (от старых к новым)
        """
        raise NotImplementedError

