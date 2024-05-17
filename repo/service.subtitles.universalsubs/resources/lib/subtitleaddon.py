# -*- coding: utf-8 -*-

import logging
import logging.config
import os
import os.path
import re
import shutil
import tempfile
from datetime import timedelta
from pathlib import Path
from typing import Dict, List
from urllib.parse import parse_qs, unquote, urlencode

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

from resources.lib.common.language import Language
from resources.lib.common.settings import Settings
from resources.lib.providers.getrequest import GetRequest
from resources.lib.providers.providersregistry import ProvidersRegistry
from resources.lib.providers.searchrequest import SearchRequest
from resources.lib.utils.compression import Compression
from resources.lib.utils.logging import init_logging_from_yaml
from resources.lib.utils.media_info import MediaInfo
from resources.lib.utils.yaml import to_yaml

FILENAME_SHOW_EPISODE_RE = re.compile(
    r"\s*(?P<show_title>.+)[\s_-]+S(?P<season_number>\d+)E(?P<episode_number>\d+)[\s_-]+(?P<title>.*)\s*",
    flags=re.IGNORECASE
)


class SubtitleAddon:

    def __init__(self) -> None:
        kodi_addon = xbmcaddon.Addon()
        self._settings: Settings = Settings()
        self._settings.addon_id = kodi_addon.getAddonInfo("id")
        self._settings.addon_path = Path(xbmcvfs.translatePath(kodi_addon.getAddonInfo("path")))
        self._settings.addon_user_path = Path(xbmcvfs.translatePath(kodi_addon.getAddonInfo("profile")))

        kodi_addon_settings = kodi_addon.getSettings()
        self._settings.include_author_on_results = kodi_addon_settings.getBool("include_author_on_results")
        self._settings.include_downloads_on_results = kodi_addon_settings.getBool(
            "include_downloads_on_results")
        self._settings.search_cache_ttl = timedelta(minutes=kodi_addon_settings.getInt("search_cache_ttl"))
        self._settings.translation_cache_ttl = timedelta(days=kodi_addon_settings.getInt("translation_cache_ttl"))
        self._settings.providers = kodi_addon_settings.getStringList("providers")
        self._settings.file_system_provider_path = Path(kodi_addon_settings.getString("file_system_provider_path"))
        self._settings.cache_whole_requests = kodi_addon_settings.getBool("cache_whole_requests")
        self._settings.exclude_splitted_subtitles = kodi_addon_settings.getBool("exclude_splitted_subtitles")
        if not self._settings.file_system_provider_path.exists() and "FileSystem" in self._settings.providers:
            self._settings.providers.remove("FileSystem")
        self._settings.translators = kodi_addon_settings.getStringList("translators")
        if len(self._settings.translators) > 0:
            self._settings.translation_extra_languages = [language for language in [
                Language.from_standard_name(lang_name)
                for lang_name in kodi_addon_settings.getStringList("translation_extra_languages")
            ] if language is not None]

        self._settings.clean_up_subtitles = kodi_addon_settings.getBool("clean_up_subtitles")
        self._settings.clean_up_ads = kodi_addon_settings.getBool("clean_up_ads")
        self._settings.clean_up_hi_markers = kodi_addon_settings.getBool("clean_up_hi_markers")
        self._settings.clean_up_rules_update_url = kodi_addon_settings.getString("clean_up_rules_update_url")
        self._settings.clean_up_rules_update_interval = timedelta(
            days=kodi_addon_settings.getInt("clean_up_rules_update_interval"))

        seven_zip_exec_path = kodi_addon_settings.getString("seven_zip_executable")
        if seven_zip_exec_path:
            Compression.seven_zip_exec_path = seven_zip_exec_path

        mkvtoolnix_path = kodi_addon_settings.getString("mkvtoolnix_path")
        if mkvtoolnix_path:
            MediaInfo.mkvtoolnix_path = mkvtoolnix_path

        init_logging_from_yaml(self._settings.addon_path.joinpath('logging.kodi.yaml'))
        self._logger = logging.getLogger('UniversalSubs')

    def __setup_user_data_directory(self) -> None:
        """ Ensures addon user data directory exists and is clean. """
        xbmcvfs.mkdirs(self._settings.addon_user_path.as_posix())
        dirs, _ = xbmcvfs.listdir(self._settings.addon_user_path.as_posix())
        for dir_name in dirs[:10]:
            try:
                dir_path = self._settings.addon_user_path.joinpath(dir_name)
                self._logger.info("Removing user temporary directory %s", dir_path)
                shutil.rmtree(dir_path, ignore_errors=True)
            except Exception:
                self._logger.warning("Failed to remove user temporary directory %s", dir_path)

    def __parse_arguments(self, args: List[str]) -> Dict[str, str]:
        parsed_args: Dict[str, str] = {}
        action_query_string = args[2].lstrip("?")
        if action_query_string:
            if action_query_string.endswith("/"):
                action_query_string = action_query_string[:-1]
            parsed = parse_qs(action_query_string)
            for k, v in parsed.items():
                parsed_args[k] = v[0]
        return parsed_args

    def __parse_search_request(self, parsed_args: Dict[str, str]) -> None:
        request = SearchRequest()
        request.max_results = xbmcaddon.Addon().getSettings().getInt("max_search_results")
        request.languages = [Language(ln) for ln in unquote(parsed_args["languages"]).split(",")]
        request.file_languages = [
            Language.from_three_letter_code(language_three_letter_code)
            for language_three_letter_code in set([
                xbmc.getInfoLabel("VideoPlayer.AudioLanguage"),
                xbmc.getInfoLabel("VideoPlayer.SubtitlesLanguage")
            ])
            if language_three_letter_code
        ]
        request.set_file_url_or_path(unquote(xbmc.Player().getPlayingFile()))
        if request.file_parsed_url.scheme == "rar":
            request.set_file_url_or_path(os.path.dirname(request.file_url[6:]))
        elif request.file_parsed_url.scheme == "stack":
            stack_path = request.file_url.split(" , ")[0]
            request.set_file_url_or_path(stack_path[8:])
        request.manual_search_text = unquote(parsed_args.get("searchstring")) \
            if parsed_args.get("searchstring", None) \
            else None
        request.year = int(xbmc.getInfoLabel("VideoPlayer.Year").strip("()")) \
            if xbmc.getInfoLabel("VideoPlayer.Year") \
            else None
        if xbmc.getInfoLabel("VideoPlayer.DBID"):
            request.title = xbmc.getInfoLabel("VideoPlayer.Title") or xbmc.getInfoLabel("VideoPlayer.OriginalTitle")
            request.show_title = xbmc.getInfoLabel("VideoPlayer.TVshowtitle")
            if request.show_title:
                show_episode = xbmc.getInfoLabel("VideoPlayer.Episode")
                if "s" in show_episode.lower():
                    request.show_season_number = 0
                    request.show_episode_number = int(show_episode[-1:])
                else:
                    request.show_season_number = int(xbmc.getInfoLabel("VideoPlayer.Season"))
                    request.show_episode_number = int(show_episode)
        else:
            filename = os.path.splitext(xbmc.getInfoLabel("VideoPlayer.Title"))[0]
            show_episode_match = FILENAME_SHOW_EPISODE_RE.match(filename)
            if show_episode_match:
                request.show_title = show_episode_match["show_title"].replace("_", " ").strip()
                request.show_season_number = int(show_episode_match["season_number"])
                request.show_episode_number = int(show_episode_match["episode_number"])
                request.title = show_episode_match["title"].replace("_", " ").strip()
            else:
                request.title = filename
        return request

    def __handle_search(self, kodi_dir_handle: int, parsed_args: Dict[str, str]) -> None:
        request = self.__parse_search_request(parsed_args)
        provider = ProvidersRegistry.build_from_settings(self._settings)
        results = provider.search(request)
        for result in results:
            list_item_text = result.title + " | " + result.release_info if result.release_info else result.title
            list_item = xbmcgui.ListItem(label=result.language.name, label2=list_item_text)
            list_item.setArt({"icon": str(int(result.rating)), "thumb": result.language.two_letter_code})
            list_item.setProperty("sync", "true" if result.is_sync else "false")
            list_item.setProperty("hearing_imp", "true" if result.is_hearing_impaired else "false")
            xbmcplugin.addDirectoryItem(
                handle=kodi_dir_handle,
                url="plugin://%s/?" % self._settings.addon_id + urlencode({
                    "search_result_id": result.id,
                    "language": result.language.name,
                    "file_url": request.file_url.encode("utf-8")
                }),
                listitem=list_item,
                isFolder=False)
        xbmcplugin.endOfDirectory(kodi_dir_handle)

    def __handle_download(self, kodi_dir_handle: int, parsed_args: Dict[str, str]) -> None:
        self.__setup_user_data_directory()
        request = GetRequest()
        request.search_result_id = parsed_args["search_result_id"]
        request.language = Language(parsed_args["language"])
        request.file_url = parsed_args["file_url"]
        provider = ProvidersRegistry.build_from_settings(self._settings)
        results = provider.get(request)
        # NOTE: it seems Kodi is unable to fetch the subtitle from where we save it unless we do it inside a temporary folder
        write_directory_path = Path(tempfile.mkdtemp(dir=self._settings.addon_user_path))
        for result in results:
            tmp_save_path = result.write_into(write_directory_path)
            if not tmp_save_path:
                continue
            list_item = xbmcgui.ListItem(label=result.file_name)
            xbmcplugin.addDirectoryItem(
                handle=kodi_dir_handle,
                url=tmp_save_path.as_posix(),
                listitem=list_item,
                isFolder=False)
            xbmcplugin.endOfDirectory(kodi_dir_handle)
            break

    def main(self, args: List[str]) -> None:
        self._logger.info("Settings: %s", to_yaml(self._settings))
        self._logger.debug("Command line args %s", to_yaml(args))
        parsed_args: Dict[str, str] = self.__parse_arguments(args)
        self._logger.debug("Parsed args %s", to_yaml(parsed_args))
        kodi_dir_handle = int(args[1])
        action = parsed_args.get("action", "Unknown")
        if action in ("search", "manualsearch"):
            # Example args:
            # search: ["plugin://service.subtitles.universalsubs/", "66", "?action=search&languages=English%2cSpanish&preferredlanguage=English", "resume:false"]
            # manualsearch: ["plugin://service.subtitles.universalsubs/", "71", "?action=manualsearch&languages=English%2cSpanish&preferredlanguage=English&searchstring=some%20test%20with%20%c2%abddd%c2%bb", "resume:false"]
            self.__handle_search(kodi_dir_handle, parsed_args)
        elif action == "download":
            # Example args:
            # download: ["plugin://service.subtitles.universalsubs/", "69", "?action=download&file_url=file%3a%2f%2f%2fG%3a%2fPeliculas%2f%2528__OK__%2529%2fHigh%2520Fidelity%2520%25282000%2529%2520%255B2160%255D%2fHigh%2520Fidelity.mkv&search_result_id=X666XODI1OTM8X-high-fidelity-2000", "resume:false"]
            self.__handle_download(kodi_dir_handle, parsed_args)
