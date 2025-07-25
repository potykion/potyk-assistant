import musicbrainzngs
import requests

class MusicBrainzClient:
    def __init__(self):
        musicbrainzngs.set_useragent("potyk-assistant", "1.0", "https://github.com/potykion/potyk-assistant")

    def get_cover_by_artist_album(self, artist: str | None, album: str | None) -> bytes | None:
        """
        Получает обложку альбома через MusicBrainz и Cover Art Archive.
        """
        if not artist or not album:
            return None
        try:
            # Поиск релиза по артисту и альбому
            result = musicbrainzngs.search_release_groups(artist=artist, releasegroup=album, limit=1)
            release_groups = result.get("release-group-list", [])
            if not release_groups:
                return None
            release_group_id = release_groups[0]["id"]
            # Получаем релизы для группы
            releases = musicbrainzngs.get_release_group_by_id(release_group_id, includes=["releases"])
            release_list = releases["release-group"].get("release-list", [])
            if not release_list:
                return None
            release_id = release_list[0]["id"]
            # Получаем обложку через Cover Art Archive
            cover_url = f"https://coverartarchive.org/release/{release_id}/front"
            resp = requests.get(cover_url)
            if resp.status_code == 200:
                return resp.content
        except Exception:
            pass
        return None