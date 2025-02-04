from jurialmunkey.parser import get_params
from tmdbhelper.lib.addon.plugin import ADDONPATH, PLUGINPATH, convert_trakt_type, convert_type, get_setting
from tmdbhelper.lib.api.request import RequestAPI
from tmdbhelper.lib.api.api_keys.mdblist import API_KEY
from tmdbhelper.lib.items.pages import PaginatedItems
from collections import namedtuple


PaginatedItemsTuple = namedtuple("PaginatedItemsTuple", "items next_page")


PARAMS_DEF = {
    'episode': {
        'info': 'details', 'tmdb_type': 'tv', 'tmdb_id': '{tmdb_id}',
        'season': '{season}', 'episode': '{episode}'
    },
    'season': {
        'info': 'episodes', 'tmdb_type': 'tv', 'tmdb_id': '{tmdb_id}',
        'season': '{season}'
    }
}


class MDbListItemMapping():
    """ Base class for inheritance in item mappers """

    def __init__(self, item, item_type=None):
        self.item = item
        self.item_type = item_type
        self.tmdb_type = convert_trakt_type(self.item_type)
        self.dbtype = convert_type(self.tmdb_type, 'dbtype')
        self.params_def = PARAMS_DEF.get(item_type)


class MDbListItemMappingBasic(MDbListItemMapping):
    """ Mapping for individual items in a list of items """

    @property
    def unique_ids(self):
        try:
            return self._unique_ids
        except AttributeError:
            return self.get_unique_ids()

    @property
    def infolabels(self):
        try:
            return self._infolabels
        except AttributeError:
            return self.get_infolabels()

    def get_unique_ids(self, unique_ids=None):
        unique_ids = unique_ids or {}
        unique_ids['tmdb'] = self.item.get('id')
        unique_ids['imdb'] = self.item.get('imdb_id')
        if self.item_type in ('season', 'episode'):
            unique_ids['tvshow.tmdb'] = self.item.get('id')
        self._unique_ids = unique_ids
        return self._unique_ids

    def get_infolabels(self, infolabels=None):
        infolabels = infolabels or {}
        infolabels['title'] = self.item.get('title')
        infolabels['year'] = self.item.get('release_year')
        infolabels['mediatype'] = self.dbtype
        if self.item_type in ('season', 'episode'):
            infolabels['season'] = self.item.get('season')
        if self.item_type == 'episode':
            infolabels['episode'] = self.item.get('episode')
        self._infolabels = infolabels
        return self._infolabels

    def get_item(self):
        base_item = {}
        base_item['label'] = self.item.get('title') or ''
        base_item['unique_ids'] = self.unique_ids
        base_item['infolabels'] = self.infolabels
        base_item['params'] = get_params(self.item, self.tmdb_type, definition=self.params_def)
        base_item['path'] = PLUGINPATH
        return base_item


class MDbListItemMappingTrakt(MDbListItemMapping):
    """ Conversion to Trakt style metadata """

    def get_item(self):
        base_item = {}
        base_item['rank'] = self.item.get('rank') or ''
        base_item['type'] = self.item_type
        main_item = base_item.setdefault(self.item_type, {})
        main_item['title'] = self.item.get('title') or ''
        main_item['year'] = self.item.get('release_year') or ''
        uids_item = main_item.setdefault('ids', {})
        uids_item['imdb'] = self.item.get('imdb_id') or ''
        uids_item['tvdb'] = self.item.get('tvdb_id') or ''
        uids_item['tmdb'] = self.item.get('id') or ''
        return base_item


class MDbListPagination():
    """ Paginates and configures items in a list. Base class for inheritance """

    def __init__(self, meta, page=1, limit: int = None):
        self.meta = meta
        self.page = page
        self.limit = limit or (20 * max(get_setting('pagemulti_trakt', 'int'), 1))

    @property
    def paginated_items(self):
        try:
            return self._paginated_items
        except AttributeError:
            self.update_pagination()
            return self._paginated_items

    @property
    def next_page(self):
        return self.paginated_items.next_page

    def get_updated_pagination(self):
        if self.limit is None:
            return PaginatedItemsTuple(self.meta, [])
        return PaginatedItems(self.meta, page=self.page, limit=self.limit)

    def update_pagination(self):
        self._paginated_items = self.get_updated_pagination()


class MDbListPaginationListLists(MDbListPagination):
    """ Paginates and configures items in a list of lists """

    @staticmethod
    def map_item(i):
        item = {}
        item['label'] = i.get('name')
        item['infolabels'] = {'plot': i.get('description'), 'studio': [i.get('user_name')]}
        item['art'] = {'icon': f'{ADDONPATH}/resources/icons/mdblist/mdblist.png'}
        item['params'] = {
            'info': 'mdblist_userlist',
            'list_name': i.get('name'),
            'list_id': i.get('id'),
            'plugin_category': i.get('name')}
        item['unique_ids'] = {
            'mdblist': i.get('id'),
            'slug': i.get('slug'),
            'user': i.get('user_id')}
        if i.get('dynamic'):
            item['params']['dynamic'] = 'true'
        return item

    @property
    def items(self):
        try:
            return self._items
        except AttributeError:
            self.update_pagination()
            return self._items

    def update_pagination(self):
        self._paginated_items = self.get_updated_pagination()
        self._items = [j for j in (self.map_item(i) for i in self.paginated_items.items) if j]


class MDbListPaginationListItems(MDbListPagination):
    """ Paginates and configures items in a list of items """

    def __init__(self, meta, page=1, limit: int = None, permitted_types: tuple = None, trakt_style: bool = False):
        super(MDbListPaginationListItems, self).__init__(meta, page=page, limit=limit)
        self.meta = [i for k, v in meta.items() for i in v if i]  # Join all content types together to mimic Trakt style combined lists TODO: Add a filter
        self.permitted_types = permitted_types or ('movie', 'show', 'season', 'episode')
        self.trakt_style = trakt_style

    @property
    def items(self):
        return self.paginated_items_dict.get('items') or []

    @property
    def movies(self):
        return self.paginated_items_dict.get('movies') or []

    @property
    def shows(self):
        return self.paginated_items_dict.get('shows') or []

    @property
    def seasons(self):
        return self.paginated_items_dict.get('seasons') or []

    @property
    def episodes(self):
        return self.paginated_items_dict.get('episodes') or []

    @property
    def item_maker(self):
        if self.trakt_style:
            return MDbListItemMappingTrakt
        return MDbListItemMappingBasic

    @property
    def paginated_items_dict(self):
        try:
            return self._paginated_items_dict
        except AttributeError:
            self.update_pagination()
            return self._paginated_items_dict

    def update_pagination(self):
        self._paginated_items = self.get_updated_pagination()

        configured = {'items': []}
        configured_items_append = configured['items'].append

        for i in self._paginated_items.items:
            i_type = i.get('mediatype', None)

            if self.permitted_types and i_type not in self.permitted_types:
                continue

            item = self.item_maker(i, item_type=i_type).get_item()

            if not item:
                continue

            # Also add item to a list only containing that item type
            # Useful if we need to only get one type of item from a mixed list (e.g. only "movies")
            configured.setdefault(f'{i_type}s', []).append(item)
            configured_items_append(item)

        self._paginated_items_dict = configured
        self._paginated_items_dict['next_page'] = self.next_page


class MDbListRatingMapping():
    ratings_translation = {
        'tomatoes': 'rottentomatoes_rating',
        'tomatoesaudience': 'rottentomatoes_usermeter'}

    def __init__(self, meta):
        self.meta = meta

    @property
    def meta_ratings(self):
        try:
            return self.meta['ratings']
        except (KeyError, TypeError):
            return []

    @property
    def ratings(self):
        try:
            return self._ratings
        except AttributeError:
            return self.get_ratings()

    def get_ratings(self):
        ratings = {}
        ratings['mdblist_rating'] = self.meta.get('score')

        for i in self.meta_ratings:
            try:
                name = i['source']
            except KeyError:
                continue
            if i.get('value'):
                ratings[self.ratings_translation.get(name) or f'{name}_rating'] = i['value']
            if i.get('votes'):
                ratings[f'{name}_votes'] = i['votes']

        self._ratings = ratings
        return self._ratings


class MDbList(RequestAPI):

    api_key = API_KEY

    def __init__(self, api_key=None):
        api_key = api_key or self.api_key

        super(MDbList, self).__init__(
            req_api_key=f'apikey={api_key}',
            req_api_name='MDbList.v2',
            req_api_url='https://api.mdblist.com')  # OLD API = https://mdblist.com/api
        MDbList.api_key = api_key

    def modify_static_list(self, list_id, media_type, media_id, media_provider='tmdb', action='add'):
        item = {f'{media_type}s': [{media_provider: media_id}]}
        path = self.get_request_url('lists', list_id, 'items', action)
        return self.get_api_request(path, postdata=item, method='json')

    def get_details(self, media_type, media_id, media_provider='tmdb'):
        return self.get_request_sc(media_provider, media_type, media_id)  # TODO: Add append_to_response=review ?

    def get_ratings(self, media_type, media_id, media_provider='tmdb'):
        response = self.get_details(media_type, media_id, media_provider=media_provider)
        response = MDbListRatingMapping(response)
        return response.ratings

    def get_list_of_lists(self, path, page=1, limit: int = None):
        response = self.get_request_sc(path, cache_refresh=True if page == 1 else False)
        response = MDbListPaginationListLists(response, page=page, limit=limit or 250)
        return response.items if not response.next_page else response.items + response.next_page

    def get_list_of_lists_search(self, query):
        return self.get_list_of_lists(path=f'lists/search?query={query}')

    def get_custom_trakt_style_list(self, list_id):
        path = f'lists/{list_id}/items'
        response = self.get_request_sc(path, cache_refresh=True)
        return self.get_paginated(response, permitted_types=('movie', 'show'), trakt_style=True)

    def get_custom_list(self, list_id, page=1, limit: int = None):
        path = f'lists/{list_id}/items'
        response = self.get_request_sc(path, cache_refresh=True if page == 1 else False)
        response = self.get_paginated(response, page=page, limit=limit)
        return response

    def get_paginated(self, response, page=1, limit: int = None, permitted_types: tuple = None, trakt_style=False):
        return MDbListPaginationListItems(response or {}, page=page, limit=limit, permitted_types=permitted_types, trakt_style=trakt_style)
