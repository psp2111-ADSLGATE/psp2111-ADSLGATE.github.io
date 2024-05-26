from typing import Union
import zipfile
import xbmc
import io
import re
from requests import Session, ConnectionError, HTTPError, ReadTimeout, Timeout, RequestException
from resources.lib.exceptions import AuthenticationError, ConfigurationError, DownloadLimitExceeded, ProviderError, \
    ServiceUnavailable, TooManyRequests, BadUsernameError
from resources.lib.cache import Cache
from resources.lib.utilities import log


API_URL = "https://api.subdl.com/api/v1/subtitles"
TMDB_API = "https://api.themoviedb.org/3/search"
CONTENT_TYPE = "application/json"
REQUEST_TIMEOUT = 30



def logging(msg):
    return log(__name__, msg)


class SubtitlesProvider:
    def __init__(self, api_key, tmdb_api_key):

        if not api_key:
            raise ConfigurationError("SubDL API must be specified")
        if not tmdb_api_key:
            raise ConfigurationError("TMDB API must be specified")

        self.api_key = api_key
        self.tmdb_api_key = tmdb_api_key
        self.request_headers = {"Content-Type": CONTENT_TYPE, "Accept": CONTENT_TYPE}
        self.session = Session()
        self.session.headers = self.request_headers
        # Use any other cache outside of module/Kodi
        self.cache = Cache(key_prefix="os_com")

    def handle_request(self, url):
        try:
            r = self.session.get(url, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
        except (ConnectionError, Timeout, ReadTimeout) as e:
            raise ServiceUnavailable(f"Unknown Error, empty response: {e.status_code}: {e!r}")
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 429:
                raise TooManyRequests()
            elif status_code == 503:
                raise ProviderError(e)
            else:
                raise ProviderError(f"Bad status code: {status_code}")
        return r.json()

    def parse_filename(self, filename):
        clean_name = re.sub(r'\.\d+p.*|\.(mkv|avi|mp4)$', '', filename)
        clean_name = re.sub(r'\(.*?\)', '', clean_name).strip()
        # Replace dots that are likely separators (not part of abbreviations)
        # Replace a dot if it's followed by an uppercase letter or at the end of the name
        clean_name = re.sub(r'\.(?=[A-Z])', ' ', clean_name)
        clean_name = re.sub(r'\.', ' ', clean_name)  # Replace remaining dots that might be separators
        clean_name = re.sub(r'\s+', ' ', clean_name)  

        # Extract year
        year_match = re.search(r'\b(19[0-9]{2}|20[0-9]{2})\b', clean_name)
        year = xbmc.getInfoLabel("VideoPlayer.Year") if year_match else None

        # Check for series and season/episode
        series_match = xbmc.getInfoLabel("VideoPlayer.TVshowtitle")
        if series_match:
            type_content = 'tv'
            seasonIdx = str(xbmc.getInfoLabel("VideoPlayer.Season"))
            episodeIdx = str(xbmc.getInfoLabel("VideoPlayer.Episode"))
            title = xbmc.getInfoLabel("VideoPlayer.OriginalTitle")
            imdbid = xbmc.getInfoLabel("VideoPlayer.IMDBNumber")
        else:
            type_content = 'movie'
            seasonIdx = None
            episodeIdx = None
            title = clean_name[:year_match.start()].strip().rstrip('.') if year_match else clean_name.rstrip('.')
            imdbid = xbmc.getInfoLabel("VideoPlayer.IMDBNumber")

        return {
            "title": title,
            "year": year,
            "type": type_content,
            "season_number": seasonIdx,
            "episode_number": episodeIdx,
            "imdb_id": imdbid
        }



    def get_tmdb_id(self, metadata):
        url = f"{TMDB_API}/{metadata['type']}?query={metadata['title']}&api_key={self.tmdb_api_key}"
        if 'year' in metadata and metadata['year']:
            url += f"&year={metadata['year']}"
        data = self.handle_request(url)
        if "results" not in data or not data["results"]:
            raise ProviderError("Invalid JSON returned by provider")
        return data["results"][0]["id"]

    def search_subtitles(self, media_data: dict):
        metadata = self.parse_filename(media_data['query'])
        tmdbID = self.get_tmdb_id(metadata)
        url = f"{API_URL}?api_key={self.api_key}&type={metadata['type']}&languages=AR&tmdb_id={tmdbID}"
        if metadata['type'] == 'tv':
            url += f"&season_number={metadata['season_number']}&episode_number={metadata['episode_number']}"
        result = self.handle_request(url)
        if "subtitles" not in result:
            raise ProviderError("Invalid JSON returned by provider")
        logging(f"Query returned {len(result['subtitles'])} subtitles")
        return result["subtitles"] if result["subtitles"] else None
    
    def download_subtitle(self, query: dict):
        download_link = "https://dl.subdl.com/" + query["file_id"]
        res = self.session.get(download_link)
        res.raise_for_status()

        try:
            # Unzip the file
            with zipfile.ZipFile(io.BytesIO(res.content)) as z:
                # Assuming there's only one file in the zip
                file_name = z.namelist()[0]
                file_content = z.read(file_name)
        except zipfile.BadZipFile as e:
            logging(f"Failed to unzip subtitle: {e}")
            raise ProviderError(f"Failed to unzip subtitle: {e}")

        return file_content
    
