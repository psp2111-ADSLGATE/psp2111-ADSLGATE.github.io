# -*- coding: utf-8 -*-
from xbmc import executebuiltin, getInfoLabel

# from modules.logger import logger


def person_search(params):
    return executebuiltin(
        "RunPlugin(plugin://plugin.video.fen/?mode=person_search_choice&query=%s)"
        % params["query"]
    )


def extras(params):
    return executebuiltin(
        "RunPlugin(%s)" % getInfoLabel("ListItem.Property(fen.extras_params)")
    )
