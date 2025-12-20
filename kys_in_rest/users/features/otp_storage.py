import secrets
import time
from typing import Dict, Optional


class OtpStorage:
    """Хранилище OTP кодов в памяти с TTL"""

    def __init__(self, ttl_seconds: int = 300):
        """
        Args:
            ttl_seconds: Время жизни OTP в секундах (по умолчанию 5 минут)
        """
        self._storage: Dict[str, tuple[int, str]] = {}  # username -> (user_id, otp, timestamp)
        self.ttl_seconds = ttl_seconds

    def generate_otp(self, username: str, user_id: int) -> str:
        """Генерирует и сохраняет OTP для пользователя"""
        # Удаляем старые записи для этого пользователя
        if username in self._storage:
            del self._storage[username]

        # Генерируем 6-значный OTP
        otp = f"{secrets.randbelow(1000000):06d}"
        timestamp = int(time.time())

        self._storage[username] = (user_id, otp, timestamp)
        return otp

    def verify_otp(self, username: str, otp: str) -> Optional[int]:
        """
        Проверяет OTP для пользователя.
        Returns:
            user_id если OTP валиден, None если невалиден или истек
        """
        if username not in self._storage:
            return None

        user_id, stored_otp, timestamp = self._storage[username]

        # Проверяем TTL
        if int(time.time()) - timestamp > self.ttl_seconds:
            del self._storage[username]
            return None

        # Проверяем OTP
        if stored_otp != otp:
            return None

        # Удаляем использованный OTP
        del self._storage[username]
        return user_id

    def cleanup_expired(self) -> None:
        """Удаляет истекшие OTP"""
        current_time = int(time.time())
        expired_usernames = [
            username
            for username, (_, _, timestamp) in self._storage.items()
            if current_time - timestamp > self.ttl_seconds
        ]
        for username in expired_usernames:
            del self._storage[username]

