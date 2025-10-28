from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def parse_utc_date(date_str: str) -> datetime:
    """Парсит дату в формате 'Sun, 19 Oct 2025 16:50:04 +0000' и возвращает datetime в UTC."""
    return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")


def to_moscow_time(utc_dt: datetime) -> datetime:
    """Конвертирует UTC datetime в московское время."""
    return utc_dt.astimezone(ZoneInfo("Europe/Moscow"))


def get_moscow_now() -> datetime:
    """Возвращает текущее время в московском часовом поясе."""
    return datetime.now(ZoneInfo("Europe/Moscow"))


def get_yesterday_moscow() -> datetime:
    """Возвращает начало вчерашнего дня по московскому времени."""
    now = get_moscow_now()
    yesterday = now - timedelta(days=1)
    return yesterday.replace(hour=0, minute=0, second=0, microsecond=0)


def get_week_ago_moscow() -> datetime:
    """Возвращает дату неделю назад по московскому времени."""
    now = get_moscow_now()
    week_ago = now - timedelta(weeks=1)
    return week_ago


def get_month_ago_moscow() -> datetime:
    """Возвращает дату месяц назад по московскому времени."""
    now = get_moscow_now()
    month_ago = now - timedelta(days=30)
    return month_ago


def is_checkin_in_period(checkin_date_str: str, period_start: datetime) -> bool:
    """Проверяет, попадает ли чекин в указанный период (по московскому времени)."""
    checkin_utc = parse_utc_date(checkin_date_str)
    checkin_moscow = to_moscow_time(checkin_utc)
    return checkin_moscow >= period_start
