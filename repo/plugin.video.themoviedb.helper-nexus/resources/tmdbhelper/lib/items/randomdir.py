import random
from tmdbhelper.lib.items.container import ContainerDirectory
from tmdbhelper.lib.addon.consts import RANDOMISED_LISTS, RANDOMISED_TRAKT
from jurialmunkey.parser import merge_two_dicts
from tmdbhelper.lib.items.routes import get_container


class ListTraktRandom(ContainerDirectory):
    def get_items(self, **kwargs):
        kwargs['info'] = RANDOMISED_TRAKT.get(kwargs.get('info'), {}).get('info')
        kwargs['randomise'] = True
        self.parent_params = kwargs
        return get_container(kwargs['info']).get_items(self, **kwargs)


class ListRandom(ContainerDirectory):
    def get_items(self, **kwargs):
        def random_from_list(i, remove_next_page=True):
            if not i or not isinstance(i, list) or len(i) < 2:
                return
            item = random.choice(i)
            if remove_next_page and isinstance(item, dict) and 'next_page' in item:
                return random_from_list(i, remove_next_page=True)
            return item

        info_model = RANDOMISED_LISTS[kwargs['info']]
        seedparams = merge_two_dicts(kwargs, info_model.get('params'))

        item = random_from_list(get_container(seedparams['info']).get_items(self, **seedparams))
        if not item:
            return

        itemparams = item.get('params', {})
        self.plugin_category = f'{item.get("label")}'
        self.parent_params = itemparams

        try:
            del self._tmdb_cache_only  # Avoid inheriting cache settings from seed item
        except AttributeError:
            pass

        return get_container(itemparams['info']).get_items(self, **itemparams)
