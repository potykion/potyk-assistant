import glob
import os
import subprocess
import sys
import tempfile

import mutagen
from PIL import Image

from kys_in_rest.core.path_utils import do_in_dir
from kys_in_rest.music.features.download_repo import DownloadRepo
from kys_in_rest.tg.entities.audio import TgAudio


class YandexMusicDownloadRepo(DownloadRepo):
    def __init__(self, token: str) -> None:
        self.token = token

    def download_audio_from_url(self, url: str) -> TgAudio:
        with tempfile.TemporaryDirectory() as temp_dir:
            with do_in_dir(temp_dir):
                command = [
                    "yandex-music-downloader",
                    "--token",
                    self.token,
                    "--quality",
                    "1",
                    "--skip-existing",
                    "--url",
                    url,
                ]
                subprocess.call(
                    command,
                    text=True,
                    shell=sys.platform == "win32",
                )
                mp3 = [
                    *glob.glob("./**/*.mp3", recursive=True),
                    *glob.glob("./**/*.m4a", recursive=True),
                ][0]
                cover = glob.glob("./**/cover.*", recursive=True)[0]
                if cover.endswith(".png"):
                    with Image.open(cover) as img:
                        rgb_img = img.convert("RGB")

                        cover_jpg = os.path.splitext(cover)[0] + ".jpg"
                        rgb_img.save(cover_jpg, "JPEG")
                else:
                    cover_jpg = cover

                with open(mp3, "rb") as mp3_file:
                    with open(cover_jpg, "rb") as cover_f:
                        audio = mp3_file.read()

                        audio_file = mutagen.File(mp3)

                        title = (
                            audio_file.get("TIT2")
                            or audio_file.get("\xa9nam")
                            or audio_file.get("TITLE", [None])
                        )[0]

                        artist = (
                            audio_file.get("TPE1")
                            or audio_file.get("\xa9ART")
                            or audio_file.get("ARTIST", [None])
                        )[0]
                        artist = artist.replace(";", ",")

                        duration = (
                            int(audio_file.info.length)
                            if hasattr(audio_file, "info")
                            else 0
                        )

                        cover_bytes = cover_f.read()
                        return TgAudio(
                            audio=audio,
                            artist=artist,
                            title=title,
                            cover=cover_bytes,
                            duration=duration,
                        )


class UrlDownloadRepo(DownloadRepo):
    def __init__(
        self,
        yandex_music_download_repo: YandexMusicDownloadRepo,
    ):
        self.yandex_music_download_repo = yandex_music_download_repo

    def download_audio_from_url(self, url: str) -> TgAudio:
        if url.startswith("https://music.yandex.ru"):
            return self.yandex_music_download_repo.download_audio_from_url(url)
        else:
            raise Exception(f"Unsupported {url=}")
