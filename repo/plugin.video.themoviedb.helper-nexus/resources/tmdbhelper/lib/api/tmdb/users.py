from tmdbhelper.lib.api.tmdb.api import TMDbAPI, TMDb
from tmdbhelper.lib.api.tmdb.userauthenticator import TMDbUserAuthenticator
from tmdbhelper.lib.api.tmdb.userlistmethods import TMDbUserListMethods
from tmdbhelper.lib.api.tmdb.useritemmethods import TMDbUserItemMethods
# from tmdbhelper.lib.addon.logger import kodi_log


API_URL = 'https://api.themoviedb.org'


class TMDbUser(TMDbAPI, TMDbUserListMethods, TMDbUserItemMethods):
    api_url = API_URL
    api_key = ''
    api_name = 'TMDbUser'

    @property
    def tmdb_api(self):
        try:
            return self._tmdb_api
        except AttributeError:
            self._tmdb_api = TMDb()
            return self._tmdb_api

    @property
    def genres(self):
        try:
            return self._genres
        except AttributeError:
            self._genres = self.tmdb_api.genres
            return self._genres

    @property
    def authenticator(self):
        try:
            return self._authenticator
        except AttributeError:
            self._authenticator = TMDbUserAuthenticator(self)
            return self._authenticator

    @property
    def authorised_headers(self):
        """ Property to get authorised token for user via authenticator """
        return {'Authorization': f'Bearer {self.authenticator.access_token}'}

    def format_authorised_path(self, path):
        return path.format(**self.authenticator.authorised_access)

    def get_request_url(self, *args, **kwargs):
        """ Wrapper to insert v4 API path into urls """
        return super(TMDbUser, self).get_request_url('4', *args, **kwargs)

    def get_authorised_response_json(self, *args, **kwargs):
        """ Method to call paths requiring user authorisation """
        return self.get_response_json(*args, headers=self.authorised_headers, **kwargs)

    def get_request_url_v3(self, *args, **kwargs):
        """ Diversion to build v3 URLs for some endpoints not supported in v4 """
        return super(TMDbUser, self).get_request_url('3', *args, **kwargs)

    def get_response_json_v3(self, *args, postdata=None, headers=None, method=None, **kwargs):
        """ Diversion to request v3 URLs for some endpoints not supported in v4 """
        kwargs = self.configure_request_kwargs(kwargs)
        return self.get_api_request_json(self.get_request_url_v3(*args, **kwargs), postdata=postdata, headers=headers, method=method)

    def get_authorised_response_json_v3(self, *args, **kwargs):
        """ Diversion to request authorised v3 URLs for some endpoints not supported in v4 """
        return self.get_response_json_v3(*args, headers=self.authorised_headers, **kwargs)
