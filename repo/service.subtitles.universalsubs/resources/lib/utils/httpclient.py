# -*- coding: utf-8 -*-

import logging
import os
import os.path
import re
import time
import urllib
import urllib.error
from datetime import timedelta
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Set, Tuple, TypeVar
from urllib.parse import unquote, urlencode, urlparse
from urllib.request import (HTTPDefaultErrorHandler, HTTPErrorProcessor,
                            HTTPHandler, HTTPRedirectHandler, HTTPSHandler,
                            OpenerDirector)
from uuid import uuid4

import chardet
from bs4 import BeautifulSoup, Tag

from resources.lib.utils.cache import Cache
from resources.lib.utils.json import from_json, to_json

HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"


T = TypeVar('T')


def select_with(self: Tag, selector, value_extractor: Callable[[Tag], T], namespaces=None, **kwargs) -> T:
    tag = self.select_one(selector, namespaces=namespaces, **kwargs)
    return value_extractor(tag) if tag else None


def select_all_with(self: Tag, selector, value_extractor: Callable[[Tag], T], namespaces=None, **kwargs) -> List[T]:
    tags = self.select(selector, namespaces=namespaces, **kwargs)
    return [value_extractor(tag) for tag in tags]


Tag.select_with = select_with
Tag.select_all_with = select_all_with


def url_encode(params_data: Dict[any, any]) -> str:
    param_tuples: List[Tuple[str, str]] = []
    for key, value in params_data.items():
        if value is None:
            continue
        if isinstance(value, list) or isinstance(value, set):
            for value_item in value:
                if value_item is None:
                    continue
                param_tuples.append(tuple([str(key), str(value_item)]))
        else:
            param_tuples.append(tuple([str(key), str(value)]))
    return urlencode(param_tuples)


def parse_content_disposition_file_name(value: str) -> str:
    token = r'[-!#-\'*+.\dA-Z^-z|~]+'
    qdtext = r'[]-~\t !#-[]'
    mimeCharset = r'[-!#-&+\dA-Z^-z]+'
    language = r'(?:[A-Za-z]{2,3}(?:-[A-Za-z]{3}(?:-[A-Za-z]{3}){,2})?|[A-Za-z]{4,8})(?:-[A-Za-z]{4})?(?:-(?:[A-Za-z]{2}|\d{3}))(?:-(?:[\dA-Za-z]{5,8}|\d[\dA-Za-z]{3}))*(?:-[\dA-WY-Za-wy-z](?:-[\dA-Za-z]{2,8})+)*(?:-[Xx](?:-[\dA-Za-z]{1,8})+)?|[Xx](?:-[\dA-Za-z]{1,8})+|[Ee][Nn]-[Gg][Bb]-[Oo][Ee][Dd]|[Ii]-[Aa][Mm][Ii]|[Ii]-[Bb][Nn][Nn]|[Ii]-[Dd][Ee][Ff][Aa][Uu][Ll][Tt]|[Ii]-[Ee][Nn][Oo][Cc][Hh][Ii][Aa][Nn]|[Ii]-[Hh][Aa][Kk]|[Ii]-[Kk][Ll][Ii][Nn][Gg][Oo][Nn]|[Ii]-[Ll][Uu][Xx]|[Ii]-[Mm][Ii][Nn][Gg][Oo]|[Ii]-[Nn][Aa][Vv][Aa][Jj][Oo]|[Ii]-[Pp][Ww][Nn]|[Ii]-[Tt][Aa][Oo]|[Ii]-[Tt][Aa][Yy]|[Ii]-[Tt][Ss][Uu]|[Ss][Gg][Nn]-[Bb][Ee]-[Ff][Rr]|[Ss][Gg][Nn]-[Bb][Ee]-[Nn][Ll]|[Ss][Gg][Nn]-[Cc][Hh]-[Dd][Ee]'
    valueChars = r'(?:%[\dA-F][\dA-F]|[-!#$&+.\dA-Z^-z|~])*'
    dispositionParm = r'[Ff][Ii][Ll][Ee][Nn][Aa][Mm][Ee]\s*=\s*(?:({token})|"((?:{qdtext}|\\\\[\t !-~])*)")|[Ff][Ii][Ll][Ee][Nn][Aa][Mm][Ee]\*\s*=\s*({mimeCharset})\'(?:{language})?\'({valueChars})|{token}\s*=\s*(?:{token}|"(?:{qdtext}|\\\\[\t !-~])*")|{token}\*\s*=\s*{mimeCharset}\'(?:{language})?\'{valueChars}'.format(**locals())
    format_args = {
        "token": token,
        "qdtext": qdtext,
        "mimeCharset": mimeCharset,
        "language": language,
        "valueChars": valueChars,
        "dispositionParm": dispositionParm,
    }
    match = re.match(
        r'(?:{token}\s*;\s*)?(?:{dispositionParm})(?:\s*;\s*(?:{dispositionParm}))*|{token}'.format(**format_args), value)
    if not match:
        return None
    elif match.group(8) is not None:
        file_name = unquote(match.group(8)).decode(match.group(7))
    elif match.group(4) is not None:
        file_name = unquote(match.group(4)).decode(match.group(3))
    elif match.group(6) is not None:
        file_name = re.sub('\\\\(.)', '\1', match.group(6))
    elif match.group(5) is not None:
        file_name = match.group(5)
    elif match.group(2) is not None:
        file_name = re.sub('\\\\(.)', '\1', match.group(2))
    else:
        file_name = match.group(1)
    file_name = os.path.basename(file_name)
    return file_name


class HttpRequest:

    def __init__(self,
                 url: str = None,
                 method: Literal['GET', 'POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE'] = 'GET',
                 data: bytes = None,
                 headers: Dict[str, str] = {},
                 follow_redirects=True,
                 throw_on_error_codes: bool = True,
                 max_retries: int = 1,
                 allow_caching: bool = True,
                 sleep_before: timedelta = None):
        self.url = url
        self.method = method
        self.data = data
        self.headers: Dict[str, str] = {k: v for k, v in headers.items()} if headers else {}
        self.follow_redirects = follow_redirects
        self.throw_on_error_codes = throw_on_error_codes
        self.max_retries = max_retries
        self.allow_caching = allow_caching
        self.sleep_before = sleep_before

    @property
    def is_relative_url(self) -> bool:
        return not re.match(r"^[a-z]+://.*$", self.url, flags=re.IGNORECASE)

    def resolve_url(self, base_url: str, force_https: bool) -> str:
        if self.is_relative_url:
            if base_url.endswith("/"):
                resolved_url = base_url + (self.url[1:] if self.url.startswith("/") else self.url)
            else:
                resolved_url = base_url + (self.url if self.url.startswith("/") else "/" + self.url)
        else:
            resolved_url = self.url
        if force_https:
            resolved_url = re.sub("^[A-z]+:", "https:", resolved_url)
        return resolved_url

    def resolve_headers(self, default_headers: Dict[str, str]) -> Dict[str, str]:
        return {**(default_headers or {}), **(self.headers or {})}

    def add_url_query_params(self, params_data: Dict[any, any]) -> None:
        encoded_query_params = url_encode(params_data)
        self.url += ("&" if "?" in self.url else "?") + encoded_query_params

    def set_urlencoded_form_data(self, form_data: Dict[any, any]) -> None:
        self.data = url_encode(form_data).encode()
        self.headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"

    def set_multipart_form_data(self, form_data: Dict[str, str], boundary: str = None) -> None:
        if not boundary:
            boundary = (str(uuid4()) + str(uuid4())).replace("-", "")
        form_item_boundary = ("--" + boundary).encode()
        form_end_boundary = ("--" + boundary + "--").encode()
        form_items_data: List[bytes] = []
        for key, value in form_data.items():
            form_items_data.append(form_item_boundary)
            form_items_data.append(("Content-Disposition: form-data; name=\"%s\"" % key).encode())
            # form_items_data.append(b"Content-Type: text/plain")
            form_items_data.append(b"")
            form_items_data.append(value.encode())
        form_items_data.append(form_end_boundary)
        form_items_data.append(b"")
        self.data = b'\r\n'.join(form_items_data)
        self.headers["Content-Type"] = "multipart/form-data; boundary=%s" % boundary

    def set_json_data(self, data: any) -> None:
        self.data = to_json(data).encode("utf-8")
        self.headers["Content-Type"] = "application/json"

    def _build_cache_key(self, resolved_url: str, resolved_headers: Dict[str, str]) -> str:
        headers = "|".join(sorted(["%s:%s" % (k, v) for k, v in resolved_headers.items()]))
        return "HttpRequest\n%s\n%s\n%s\n%s\n%s\n%s" % (
            self.method,
            resolved_url,
            headers,
            self.follow_redirects,
            self.throw_on_error_codes,
            # base64.b64encode(self.data) if self.data else '',
            str(self.data) if self.data else '')


class HttpResponse:

    _logger: logging.Logger = logging.getLogger('UniversalSubs.HttpResponse')

    def __init__(self,
                 request: HttpRequest,
                 status_code: int,
                 headers: Dict[str, List[str]],
                 data_reader: Callable[[], bytes],
                 final_request_url: str = None):
        self._request = request
        self._status_code = status_code
        self._data: bytes = None
        self._data_reader = data_reader
        self._headers = headers
        self._final_request_url = final_request_url or request.url

    @property
    def request(self) -> HttpRequest:
        return self._request

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def has_error_code(self) -> bool:
        return self._status_code >= 400

    @property
    def final_request_url(self) -> str:
        return self._final_request_url

    @property
    def file_name(self) -> bool:
        content_disposition = self.get_header_value('Content-Disposition')
        if content_disposition:
            parsed_file_name = parse_content_disposition_file_name(content_disposition)
            if parsed_file_name:
                return parsed_file_name
        parsed_final_request_path = unquote(urlparse(self.final_request_url).path).strip('/')
        return os.path.split(parsed_final_request_path)[1]

    def get_data_as_text(self, encoding: str = None, ignore_decode_errors: bool = True) -> str:
        if not encoding:
            encoding = chardet.detect(self.data)["encoding"] or "utf-8"
        return self.data.decode(encoding, "ignore" if ignore_decode_errors else "strict")

    def get_data_as_html(self, encoding: str = None, ignore_decode_errors: bool = True) -> BeautifulSoup:
        return BeautifulSoup(self.get_data_as_text(encoding, ignore_decode_errors), 'html5lib')

    def get_data_as_json(self, encoding: str = None, ignore_decode_errors: bool = True) -> Any:
        return from_json(self.get_data_as_text(encoding, ignore_decode_errors))

    def get_header_names(self) -> Set[str]:
        return self._headers.keys()

    def get_header_value(self, header_name: str, throw_if_many=False) -> str:
        header_values = self._headers.get(header_name, [])
        if throw_if_many and len(header_values) > 1:
            raise Exception("Read single value for header %s where many exists." % header_name)
        return header_values[0] if header_values else None

    def get_header_values(self, header_name: str) -> List[str]:
        return self._headers.get(header_name, [])

    @property
    def data(self) -> bytes:
        if not self._data and self._data_reader:
            self._data = self._data_reader()
        return self._data

    def write_into(self, target_file_path: Path) -> None:
        try:
            with open(target_file_path, "wb") as file:
                file.write(self.data)
            return target_file_path
        except Exception as e:
            self._logger.fatal("Error writing HTTP response into target path '%s'" % target_file_path, exc_info=True)
            raise e

    def _build_cache_value(self) -> Dict[str, any]:
        return {
            "status_code": self.status_code,
            "headers": self._headers,
            "data": self.data,
            "final_request_url": self.final_request_url
        }


class HTTPProcessor(HTTPRedirectHandler):

    def __init__(self, cookiejar: CookieJar, follow_redirects: bool, throw_on_error_codes: bool):
        assert cookiejar is not None
        self._cookiejar = cookiejar
        self._follow_redirects = follow_redirects
        self._throw_on_error_codes = throw_on_error_codes

    def http_request(self, request):
        self._cookiejar.add_cookie_header(request)
        return request

    def http_response(self, request, response):
        self._cookiejar.extract_cookies(response, request)
        response.effective_request_url = request.full_url
        code, msg, hdrs = response.code, response.msg, response.info()
        if (100 <= code < 300):  # non error codes
            return response
        if (300 <= code < 400):  # redirect codes
            if not self._follow_redirects:
                return response
            return self.parent.error('http', request, response, code, msg, hdrs)
        if not self._throw_on_error_codes:  # error codes
            return response
        return self.parent.error('http', request, response, code, msg, hdrs)

    https_request = http_request
    https_response = http_response


def build_opener(cookiejar: CookieJar, follow_redirects: bool, throw_on_error_codes: bool) -> OpenerDirector:
    opener = OpenerDirector()
    # [ProxyHandler, UnknownHandler, HTTPHandler, HTTPSHandler,
    # HTTPDefaultErrorHandler, HTTPRedirectHandler,
    # HTTPErrorProcessor, DataHandler]
    opener.add_handler(HTTPHandler())
    opener.add_handler(HTTPSHandler())
    opener.add_handler(HTTPProcessor(cookiejar, follow_redirects, throw_on_error_codes))
    opener.add_handler(HTTPDefaultErrorHandler())
    return opener


class HttpClient():

    def __init__(self,
                 base_url: str = None,
                 default_headers: Dict[str, str] = {"User-Agent": HTTP_USER_AGENT},
                 cache: Cache = None,
                 force_https: bool = False,
                 retry_delay: timedelta = timedelta(seconds=2)):
        self._logger: logging.Logger = logging.getLogger("UniversalSubs.HttpClient")
        self._cache = cache
        self._cookiejar = CookieJar()
        self._urlopeners: Dict[str, OpenerDirector] = {}
        for follow_redirects in [True, False]:
            for throw_on_error_codes in [True, False]:
                urlopener = build_opener(self._cookiejar, follow_redirects, throw_on_error_codes)
                self._urlopeners["%s:%s" % (follow_redirects, throw_on_error_codes)] = urlopener
        self.base_url: str = base_url
        self.default_headers: Dict[str, str] = {k: v for k, v in default_headers.items()} if default_headers else {}
        self.force_https: bool = force_https
        self.retry_delay = retry_delay

    def exchange(self, request: HttpRequest) -> HttpResponse:
        resolved_url = request.resolve_url(self.base_url, self.force_https)
        resolved_headers = request.resolve_headers(self.default_headers)
        if self._cache and request.allow_caching:
            cache_key = request._build_cache_key(resolved_url, resolved_headers)
            cache_value: Dict[str, Any] = self._cache.get(cache_key)
            if cache_value:
                self._logger.info("Processing request %s %s (FOUND IN CACHE)" %
                                  (request.method, resolved_url))
                return HttpResponse(
                    request,
                    cache_value["status_code"],
                    cache_value["headers"],
                    lambda: cache_value["data"],
                    cache_value["final_request_url"])
            response = self.__exchange_impl(request, resolved_url, resolved_headers, request.max_retries)
            self._cache.set(cache_key, response._build_cache_value())
            # assert self._cache.get(cache_key)
            return response
        else:
            return self.__exchange_impl(request, resolved_url, resolved_headers, request.max_retries)

    def __exchange_impl(self, request: HttpRequest, resolved_url: str, resolved_headers: Dict[str, str], pending_retries: int) -> HttpResponse:
        if request.sleep_before:
            time.sleep(request.sleep_before.total_seconds())
        urllib_request = urllib.request.Request(resolved_url)
        urllib_request.method = request.method
        urllib_request.data = request.data
        for key, value in resolved_headers.items():
            urllib_request.add_header(key, value)
        try:
            self._logger.info("Processing request %s %s (pending retries: %s)" %
                              (request.method, resolved_url, pending_retries))
            urlopener = self._urlopeners["%s:%s" % (request.follow_redirects, request.throw_on_error_codes)]
            urllib_response = urlopener.open(urllib_request)
            return HttpResponse(
                request,
                urllib_response.getcode(),
                {hn: urllib_response.headers.get_all(hn) for hn in urllib_response.headers.keys()},
                lambda: urllib_response.read(),
                urllib_response.effective_request_url)
        except urllib.error.HTTPError as e:
            self._logger.error("Error processing request %s %s (HTTP status: %d, Body: %s)" %
                               (request.method, resolved_url, e.code, e.read().decode("utf-8", errors="ignore")), exc_info=True, stack_info=False)
            if pending_retries:
                if self.retry_delay:
                    time.sleep(self.retry_delay.total_seconds())
                return self.__exchange_impl(request, resolved_url, resolved_headers, pending_retries - 1)
            raise e
        except urllib.error.URLError as e:
            self._logger.error("Error processing request %s %s (connection error)" %
                               (request.method, resolved_url), exc_info=True, stack_info=False)
            if pending_retries:
                if self.retry_delay:
                    time.sleep(self.retry_delay.total_seconds())
                return self.__exchange_impl(request, resolved_url, resolved_headers, pending_retries - 1)
            raise e
        except Exception as e:
            self._logger.error("Error processing request %s %s: %s" % (request.method, resolved_url, e), exc_info=True)
            raise e
