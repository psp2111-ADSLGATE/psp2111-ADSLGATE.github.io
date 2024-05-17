# -*- coding: utf-8 -*-

import logging
from typing import Dict, List

from resources.lib.common.settings import Settings
from resources.lib.providers.addic7edsourceprovider import \
    Addic7edSourceProvider
from resources.lib.providers.cleanupdecoratorprovider import \
    CleanupDecoratorProvider
from resources.lib.providers.compositeprovider import CompositeProvider
from resources.lib.providers.filesystemsourceprovider import \
    FileSystemSourceProvider
from resources.lib.providers.localsourceprovider import LocalSourceProvider
from resources.lib.providers.opensubtitlessourceprovider import \
    OpenSubtitlesSourceProvider
from resources.lib.providers.podnapisisourceprovider import \
    PodnapisiSourceProvider
from resources.lib.providers.provider import Provider
from resources.lib.providers.subdivxsourceprovider import SubDivXSourceProvider
from resources.lib.providers.subscenesourceprovider import \
    SubsceneSourceProvider
from resources.lib.providers.translationsdecoratorprovider import \
    TranslationsDecoratorProvider
from resources.lib.translation.translatorsregistry import TranslatorsRegistry


class ProvidersRegistry:

    def __init__(self, settings: Settings):
        self._logger: logging.Logger = logging.getLogger("UniversalSubs.ProvidersRegistry")
        self._providers: Dict[str, Provider] = {
            provider.name: provider
            for provider in [
                PodnapisiSourceProvider(settings),
                SubsceneSourceProvider(settings),
                SubDivXSourceProvider(settings),
                OpenSubtitlesSourceProvider(settings),
                Addic7edSourceProvider(settings),
                LocalSourceProvider(settings),
                FileSystemSourceProvider(settings),
            ]
        }

    def get_provider(self, name: str) -> Provider:
        return self._providers[name]

    def get_providers(self, names: List[str]) -> List[Provider]:
        return [self._providers[name] for name in names]

    @staticmethod
    def __build_from_source_providers(settings: Settings) -> Provider:
        providersRegistry = ProvidersRegistry(settings)
        if len(settings.providers) == 1:
            return providersRegistry.get_provider(settings.providers[0])
        return CompositeProvider(providersRegistry.get_providers(settings.providers))

    @staticmethod
    def __build_from_translators(provider: Provider, settings: Settings) -> Provider:
        if not settings.translators:
            return provider
        translators_registry = TranslatorsRegistry(settings)
        translators = translators_registry.get_translators(settings.translators)
        return TranslationsDecoratorProvider(provider, translators, settings.translation_extra_languages)

    @staticmethod
    def __build_from_cleanup(provider: Provider, settings: Settings) -> Provider:
        if not settings.clean_up_subtitles:  # not settings.clean_up_ads and not settings.clean_up_hi_markers:
            return provider
        return CleanupDecoratorProvider(provider, settings)

    @staticmethod
    def build_from_settings(settings: Settings) -> Provider:
        provider = ProvidersRegistry.__build_from_source_providers(settings)
        provider = ProvidersRegistry.__build_from_translators(provider, settings)
        provider = ProvidersRegistry.__build_from_cleanup(provider, settings)
        return provider
