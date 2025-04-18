# Module: default
# Author: jurialmunkey
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
from tmdbhelper.lib.script.method.decorators import is_in_kwargs, get_tmdb_id
from tmdbhelper.lib.addon.plugin import get_localized


TMDB_USER_API_ROUTES = {
    # 'add_favorite': {'func': 'add_favorite', 'name': get_localized(32490)},
    # 'add_watchlist': {'func': 'add_watchlist', 'name': get_localized(32291)},
    # 'del_favorite': {'func': 'del_favorite', 'name': get_localized(32491)},
    # 'del_watchlist': {'func': 'del_watchlist', 'name': get_localized(32292)},
    'modify_watchlist': {'func': 'modify_watchlist', 'name': get_localized(32526)},
    'modify_favorite': {'func': 'modify_favorite', 'name': get_localized(32525)},
    'modify_list': {'func': 'modify_list', 'name': get_localized(32523)},
}


def select_sync_type():
    choices = [k for k in TMDB_USER_API_ROUTES.keys()]
    d_items = [TMDB_USER_API_ROUTES[k]['name'] for k in choices]
    from xbmcgui import Dialog
    x = Dialog().select(get_localized(32522), d_items)
    if x == -1:
        return
    return choices[x]


@is_in_kwargs({'tmdb_type': ['movie', 'tv']})
@get_tmdb_id
def sync_tmdb(tmdb_type=None, tmdb_id=None, season=None, episode=None, sync_type=None, **kwargs):
    sync_type = sync_type or select_sync_type()
    if sync_type not in TMDB_USER_API_ROUTES:
        return
    return sync_tmdb_item(tmdb_type=tmdb_type, tmdb_id=tmdb_id, season=season, episode=episode, sync_type=sync_type, **kwargs)


def sync_tmdb_item(tmdb_type=None, tmdb_id=None, season=None, episode=None, sync_type=None, **kwargs):
    from tmdbhelper.lib.api.tmdb.users import TMDbUser
    tmdb_user_api = TMDbUser()
    func = getattr(tmdb_user_api, TMDB_USER_API_ROUTES[sync_type]['func'])
    func(tmdb_type=tmdb_type, tmdb_id=tmdb_id, season=season, episode=episode)
