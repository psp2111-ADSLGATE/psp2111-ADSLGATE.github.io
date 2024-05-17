# -*- coding: utf-8 -*-

import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Literal, Tuple

from resources.lib.common.language import Language
from resources.lib.utils.json import from_json
from resources.lib.utils.process import Process


class StreamInfo:

    def __init__(self, id: str, language: Language, type: Literal['video', 'audio', 'subtitles'], sub_type: str, name: str) -> None:
        self.id: str = id
        self.language: Language = language
        self.type: Literal['video', 'audio', 'subtitles'] = type
        self.sub_type: str = sub_type
        self.name: str = name


class MediaInfo:

    _logger: logging.Logger = logging.getLogger("UniversalSubs.MediaInfo")

    mkvtoolnix_path: Path = Path("C:/Program Files/MKVToolNix") if os.name == 'nt' else Path("/usr/bin")

    @staticmethod
    def build_mkvtoolnix_exec_path(exec_name: str) -> Path:
        return MediaInfo.mkvtoolnix_path.joinpath(Process.build_exec_file_path(exec_name))

    @staticmethod
    def process_creation_flags() -> int:
        return subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

    @staticmethod
    def parse_streams(file_path: Path) -> List[StreamInfo]:
        if os.path.splitext(file_path)[1].lower() != '.mkv':
            return []
        try:
            file_info_json = Process.capture_output(
                [MediaInfo.build_mkvtoolnix_exec_path("mkvmerge"), "-J", file_path],
                throw_on_error=True)
            file_tracks = from_json(file_info_json)['tracks']
            streams_info = [
                StreamInfo(
                    str(file_track["id"]),
                    Language.from_two_letter_code(file_track["properties"].get("language_ietf", 'xx')),
                    file_track["type"],
                    file_track["codec"],
                    file_track["properties"].get("track_name", None))
                for file_track in file_tracks
            ]
            return streams_info
        except Exception as e:
            MediaInfo._logger.error("Error parsing streams for \"%s\"" % file_path, exc_info=True)
            return []

    @staticmethod
    def parse_subtitle_streams(file_path: Path) -> List[StreamInfo]:
        return [stream for stream in MediaInfo.parse_streams(file_path) if stream.type == 'subtitles']

    def extract_subtitle_stream(file_path: Path, stream_id: str) -> Tuple[str, bytes]:  # file_name, file_content
        stream_info = next(stream for stream in MediaInfo.parse_subtitle_streams(file_path) if stream.id == stream_id)
        if not stream_info:
            return [None, None]
        temp_subtitle_directory_path = Path(tempfile.mkdtemp())
        try:
            basename = os.path.basename(os.path.splitext(file_path)[0])
            file_name = "{basename}.{language_code}.{extension}".format(
                basename=basename,
                language_code=stream_info.language.two_letter_code,
                extension=stream_info.sub_type.split("/")[1].lower())
            temp_subtitle_file_path = temp_subtitle_directory_path.joinpath(file_name)
            track_id_and_file_name = "{id}:{file_path}".format(id=stream_info.id, file_path=temp_subtitle_file_path)
            Process.run([
                MediaInfo.build_mkvtoolnix_exec_path("mkvextract"), file_path, "tracks", track_id_and_file_name],
                throw_on_error=True)
            with open(temp_subtitle_file_path, 'rb') as temp_subtitle_file:
                temp_subtitle_file_content: bytes = temp_subtitle_file.read()
                return [file_name, temp_subtitle_file_content]
        except Exception as e:
            MediaInfo._logger.error("Error extracting subtitle stream %s for \"%s\"" %
                                    (stream_id, file_path), exc_info=True)
            return [None, None]
        finally:
            try:
                shutil.rmtree(temp_subtitle_directory_path, ignore_errors=True)
            except Exception:
                pass
