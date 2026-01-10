import os
import asyncio
from typing import Any

import dotenv
import flask
from flask import Flask, Response
from flask_cors import CORS
from telegram import Bot
from telegram.error import TelegramError

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.beer.features.beer_sync import BeerSync
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.health.features.weight_repo import WeightRepo
from kys_in_rest.movies.features.movie_repo import MovieRepo
from kys_in_rest.users.features.otp_storage import OtpStorage


def create_app() -> Flask:
    dotenv.load_dotenv(root_dir / ".env")

    ioc = make_ioc(
        db_path=str(root_dir / os.environ["DB"]),
        tg_admins=list(map(int, os.environ["TG_ADMINS"].split(","))),
        yandex_music_token=os.environ["YANDEX_MUSIC_TOKEN"],
        zen_money_token=os.environ["ZEN_MONEY_TOKEN"],
        untappd_cookie=os.environ["UNTAPPD_COOKIE"],
    )

    app = Flask(__name__)
    CORS(app)

    # Инициализируем хранилище OTP
    otp_storage = OtpStorage(ttl_seconds=300)  # 5 минут
    tg_token = os.environ.get("TG_TOKEN", "")
    bot = Bot(token=tg_token) if tg_token else None
    
    # Функция для получения username бота (ленивая загрузка)
    def get_bot_username() -> str | None:
        if not bot:
            return None
        try:
            async def fetch_username() -> str | None:
                if not bot:
                    return None
                bot_info = await bot.get_me()
                return bot_info.username
            return asyncio.run(fetch_username())
        except Exception:
            return None

    @app.route("/weight")
    def weight() -> flask.Response:
        entries = ioc.resolve(WeightRepo).list_weight_entries()
        return flask.jsonify([e.model_dump() for e in entries])

    @app.route("/movies")
    def movies() -> flask.Response:
        movies_list = ioc.resolve(MovieRepo).list_movies()
        return flask.jsonify([m.model_dump() for m in movies_list])

    @app.route("/movies", methods=["POST"])
    def create_movie() -> tuple[flask.Response, int]:
        movie_repo = ioc.resolve(MovieRepo)
        data = flask.request.get_json()
        if not data:
            return flask.jsonify({"error": "No JSON data provided"}), 400

        from kys_in_rest.movies.entities.movie import Movie

        movie = Movie(**data)
        created_movie = movie_repo.create_movie(movie)
        return flask.jsonify(created_movie.model_dump()), 201

    @app.route("/movies/<int:movie_id>", methods=["PUT"])
    def update_movie(movie_id: int) -> tuple[flask.Response, int]:
        movie_repo = ioc.resolve(MovieRepo)
        existing_movie = movie_repo.get_by_id(movie_id)
        if not existing_movie:
            return flask.jsonify({"error": "Movie not found"}), 404

        data = flask.request.get_json()
        if not data:
            return flask.jsonify({"error": "No JSON data provided"}), 400

        from kys_in_rest.movies.entities.movie import Movie

        movie = Movie(id=movie_id, **data)
        movie_repo.update_movie(movie)
        updated_movie = movie_repo.get_by_id(movie_id)
        return flask.jsonify(updated_movie.model_dump() if updated_movie else {}), 200

    # todo auth required
    @app.route("/beer/sync", methods=["POST"])
    def beer_sync() -> flask.Response:
        beer_sync = ioc.resolve(BeerSync)
        checkins = beer_sync.do("potykion")
        return flask.jsonify([c.model_dump() for c in checkins])

    @app.route("/beer/sync_first_time", methods=["POST"])
    def beer_sync_first_time() -> flask.Response:
        beer_sync = ioc.resolve(BeerSync)
        checkins = beer_sync.first_time("potykion")
        return flask.jsonify([c.model_dump() for c in checkins])

    @app.route("/auth/telegram", methods=["POST"])
    def auth_telegram() -> tuple[Response, int] | Response:
        data = flask.request.get_json()
        if not data:
            return flask.jsonify({"error": "No JSON data provided"}), 400

        tg_user_id = data.get("id")
        if not tg_user_id:
            return flask.jsonify({"error": "Telegram user ID is required"}), 400

        tg_admins = ioc.resolve("tg_admins")
        is_admin = int(tg_user_id) in tg_admins

        return flask.jsonify({
            "user": data,
            "is_admin": is_admin,
        }), 200

    @app.route("/auth/telegram/otp/request", methods=["POST"])
    def auth_telegram_otp_request() -> tuple[Response, int] | Response:
        """Запрашивает OTP для авторизации через Telegram бота"""
        data = flask.request.get_json()
        if not data:
            return flask.jsonify({"error": "No JSON data provided"}), 400

        username = data.get("username", "").strip().lstrip("@")
        if not username:
            return flask.jsonify({"error": "Username is required"}), 400

        if not bot:
            return flask.jsonify({"error": "Telegram bot is not configured"}), 500

        try:
            # Пытаемся получить user_id по username через Bot API
            # Для этого нужно, чтобы пользователь уже взаимодействовал с ботом
            # Используем getChat для получения информации о пользователе
            async def get_user_id() -> int | None:
                if not bot:
                    return None
                try:
                    # Пытаемся получить информацию о пользователе
                    # Это работает только если пользователь уже писал боту
                    chat = await bot.get_chat(f"@{username}")
                    return chat.id
                except TelegramError:
                    # Если не получилось, возвращаем None
                    # В этом случае пользователю нужно будет написать боту
                    return None

            user_id = asyncio.run(get_user_id())

            if user_id is None:
                return flask.jsonify({
                    "error": "User not found. Please start a conversation with the bot first.",
                    "bot_username": get_bot_username(),
                }), 404

            # Генерируем OTP
            otp = otp_storage.generate_otp(username, user_id)

            # Отправляем OTP через бота
            async def send_otp() -> bool:
                if not bot:
                    return False
                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"Ваш код для входа на potyk.io:\n\n<code>{otp}</code>\n\nКод действителен 5 минут.",
                        parse_mode="HTML"
                    )
                    return True
                except TelegramError as e:
                    print(f"Error sending OTP: {e}")
                    return False

            sent = asyncio.run(send_otp())
            if not sent:
                return flask.jsonify({"error": "Failed to send OTP. Please check if you started a conversation with the bot."}), 500

            return flask.jsonify({
                "message": "OTP sent successfully",
            }), 200

        except Exception as e:
            return flask.jsonify({"error": str(e)}), 500

    @app.route("/auth/telegram/otp/verify", methods=["POST"])
    def auth_telegram_otp_verify() -> tuple[Response, int] | Response:
        """Проверяет OTP и возвращает данные пользователя"""
        data = flask.request.get_json()
        if not data:
            return flask.jsonify({"error": "No JSON data provided"}), 400

        username = data.get("username", "").strip().lstrip("@")
        otp = data.get("otp", "").strip()

        if not username or not otp:
            return flask.jsonify({"error": "Username and OTP are required"}), 400

        # Проверяем OTP
        user_id = otp_storage.verify_otp(username, otp)

        if user_id is None:
            return flask.jsonify({"error": "Invalid or expired OTP"}), 400

        # Получаем информацию о пользователе через Bot API
        if not bot:
            return flask.jsonify({"error": "Telegram bot is not configured"}), 500

        try:
            async def get_user_info() -> dict[str, Any]:
                if not bot:
                    return {
                        "id": user_id,
                        "first_name": username,
                        "username": username,
                    }
                try:
                    chat = await bot.get_chat(user_id)
                    return {
                        "id": chat.id,
                        "first_name": chat.first_name or "",
                        "last_name": chat.last_name or "",
                        "username": chat.username or "",
                    }
                except TelegramError:
                    # Если не получилось получить информацию, используем базовые данные
                    return {
                        "id": user_id,
                        "first_name": username,
                        "username": username,
                    }

            user_info = asyncio.run(get_user_info())

            # Проверяем, является ли пользователь админом
            tg_admins = ioc.resolve("tg_admins")
            is_admin = user_id in tg_admins

            return flask.jsonify({
                "user": user_info,
                "is_admin": is_admin,
            }), 200

        except Exception as e:
            return flask.jsonify({"error": str(e)}), 500

    return app
