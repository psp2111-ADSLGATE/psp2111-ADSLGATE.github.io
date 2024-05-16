
from typing import Union
import zipfile
import difflib
import io
import re
import json
from requests import Session, ConnectionError, HTTPError, ReadTimeout, Timeout, RequestException
from resources.lib.exceptions import AuthenticationError, ConfigurationError, DownloadLimitExceeded, ProviderError, \
    ServiceUnavailable, TooManyRequests, BadUsernameError
from resources.lib.cache import Cache
from resources.lib.utilities import log

API_URL = "https://api.subsource.net/api"

def logging(msg):
    return log(__name__, msg)

class SubtitlesProvider:
    def __init__(self):
        self.request_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://subsource.net',
            'priority': 'u=1, i',
            'referer': 'https://subsource.net/',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            }
        self.session = Session()
        self.session.headers = self.request_headers
        # Use any other cache outside of module/Kodi
        self.cache = Cache(key_prefix="os_com")

    def handle_request(self, url, data):
        try:
            r = self.session.post(url, data=json.dumps(data))
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
        filename = re.sub(r'\[.*?\]', '', filename).strip()
        clean_name = re.sub(r'\.\d+p.*|\.(mkv|avi|mp4)$', '', filename)
        clean_name = re.sub(r'\(.*?\)', '', clean_name).strip()
        clean_name = re.sub(r'\.(?=[A-Z])', ' ', clean_name)
        clean_name = re.sub(r'\.', ' ', clean_name)  # Replace remaining dots that might be separators
        clean_name = re.sub(r'\s+', ' ', clean_name)  
        year_match = re.search(r'\b(19[0-9]{2}|20[0-9]{2})\b', clean_name)
        year = year_match.group(0) if year_match else None
        series_match = re.search(r'S(\d+)E(\d+)', filename, re.IGNORECASE)
        if series_match:
            type_content = 'TVSeries'
            seasonIdx = int(series_match.group(1))
            episodeIdx = int(series_match.group(2))
            title = re.sub(r'\s*S\d+E\d+.*', '', clean_name[:year_match.start() if year_match else None]).strip()
            title = title.rstrip('.').rstrip()
        else:
            type_content = 'Movie'
            seasonIdx = None
            episodeIdx = None
            title = clean_name[:year_match.start()].strip().rstrip('.') if year_match else clean_name.rstrip('.')

        return {
            "title": title,
            "year": year,
            "type": type_content,
            "season_number": seasonIdx,
            "episode_number": episodeIdx
        }

    def search_subtitles(self, media_data: dict):
        metadata = self.parse_filename(media_data['query'])
        data = {'query': metadata['title']}
        ep_index = None
        if metadata['type'] == 'TVSeries':
            ep_index = f"S{metadata['season_number']:02d}E{metadata['episode_number']:02d}"
            logging(f"Ep index: {ep_index}")
        response = self.handle_request(API_URL+"/searchMovie", data=data)
        logging(f"Search response: {response}")
        if response['success']:
            for item in response['found']:
                logging(f"Item: {item}")
                logging(f"Metadata: {metadata}")
                if self.is_match_item(item, metadata):
                    data = {'movieName': item['linkName']}
                    if metadata['type'] == 'TVSeries':
                         data['season'] = f"season-{metadata['season_number']}"
                    response = self.handle_request(API_URL+"/getMovie", data=data)
                    logging(f"Get movie response: {response}")
                    logging(f"Ep index: {response['success']}")
                    if response['success']:
                        return self.filter_subs_by_language_and_epindex(response['subs'], 'Arabic', ep_index)
                    else: 
                        return None
            return None 


    def filter_subs_by_language_and_epindex(self, subs_list, target_language, ep_index=None):
        if ep_index:
            return [sub for sub in subs_list if sub['lang'] == target_language and ep_index in sub['releaseName']]
        else:
            return [sub for sub in subs_list if sub['lang'] == target_language]
        
    def is_match_item(self, item, metadata):
        return self.is_match_year and self.is_match_title(item['title'], metadata['title'])

    def is_match_year(self, item, metadata):
        return metadata['year'] is None or str(item['releaseYear']) == metadata['year']

    def is_match_title(self, query, title):
        return difflib.SequenceMatcher(None, query, title).ratio() > 0.7

    def download_subtitle(self, query: dict):
        data = {"id": query["file_id"]}
        download_link = API_URL + "/downloadSub"
        res = self.session.post(url=download_link, data=json.dumps(data))
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
    
