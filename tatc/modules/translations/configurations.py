from __future__ import annotations

from functools import cached_property, lru_cache
from os import environ
from typing import Generator, Union

from tatc.core import (
    Environment, TatcApplicationConfiguration, TatcChannelConfiguration, TatcChannelModuleConfiguration
)
from tatc.modules.translations.constants import *
from tatc.utilities import Boolean, String

import translators as ts


@lru_cache(maxsize=1)
def environment() -> TatcTranslationChannelModuleEnvironment:
    return TatcTranslationChannelModuleEnvironment()


class TatcTranslationChannelModuleEnvironment(Environment):
    @cached_property
    def __default_ignore_words(self) -> set[str]:
        return set([
            word.strip() for word in environ.get(DEFAULT_IGNORE_WORDS, '').split(',')
        ])

    @cached_property
    def low_memory_mode(self) -> True:
        return Boolean.parse(environ.get(LOW_MEMORY_MODE, 'true'))

    @cached_property
    def default_translation_engine(self) -> str:
        return environ.get(DEFAULT_TRANSLATION_ENGINE, 'google')

    @property
    def default_ignore_words(self) -> list[str]:
        return list(self.__default_ignore_words)


class TatcTranslationChannelModuleConfiguration(TatcChannelModuleConfiguration):
    """
    Per-channel configuration object for the translation module
    """
    def __init__(self, channel_configuration: TatcChannelConfiguration):
        super().__init__(TRANSLATIONS, channel_configuration)

    @property
    def supported_keys(self) -> list[str]:
        return [
            ENABLED,
            TRANSLATION_ENGINE,
            TARGET_LANGUAGES,
            IGNORE_LANGUAGES,
            SANITIZE_EMOJIS,
            SANITIZE_USERNAMES,
            IGNORE_WORDS,
            DEBUG_MODE
        ]

    @property
    def enabled(self) -> bool:
        return self.data.setdefault(ENABLED, True) or False

    @property
    def translation_engine(self) -> str:
        return self.data.setdefault(TRANSLATION_ENGINE, None) or environment().default_translation_engine
    
    @property
    def target_languages(self) -> list[str]:
        return self.data.setdefault(TARGET_LANGUAGES, []) or []

    @property
    def ignore_languages(self) -> list[str]:
        return self.data.setdefault(IGNORE_LANGUAGES, []) or []

    @property
    def debug_mode(self) -> bool:
        return self.data.setdefault(DEBUG_MODE, False) or False

    @property
    def sanitize_emojis(self) -> bool:
        return self.data.setdefault(SANITIZE_EMOJIS, True) or False

    @property
    def ignore_words(self) -> list[str]:
        return self.data.setdefault(IGNORE_WORDS, environment().default_ignore_words)

    @property
    def sanitize_usernames(self) -> bool:
        return self.data.setdefault(SANITIZE_USERNAMES, False) or False

    @enabled.setter
    def enabled(self, value: bool):
        self.data[ENABLED] = Boolean.parse(value)

    @translation_engine.setter
    def translation_engine(self, value: str):
        self.data[TRANSLATION_ENGINE] = value or environment().default_translation_engine

    @target_languages.setter
    def target_languages(self, value: list[str]):
        self.data[TARGET_LANGUAGES] = list(set(
            String.strips(value)
        ))

    @ignore_languages.setter
    def ignore_languages(self, value: list[str]):
        self.data[IGNORE_LANGUAGES] = list(set(
            String.strips(value)
        ))

    @ignore_words.setter
    def ignore_words(self, value: list[str]):
        self.data[IGNORE_WORDS] = list(set(
            String.strips(value)
        ))

    @debug_mode.setter
    def debug_mode(self, value: bool):
        self.data[DEBUG_MODE] = Boolean.parse(value)

    @sanitize_emojis.setter
    def sanitize_emojis(self, value: bool):
        self.data[SANITIZE_EMOJIS] = Boolean.parse(value)

    @sanitize_usernames.setter
    def sanitize_usernames(self, value: bool):
        self.data[SANITIZE_USERNAMES] = Boolean.parse(value)

    @property
    def supported_languages(self):
        return self.__supported_language(self.translation_engine)

    @property
    def supported_engines(self):
        return self.__supported_engines()

    @lru_cache(maxsize=1)
    def __supported_language(self, translation_engine: str):
        return ts.get_languages(translator=translation_engine)

    @lru_cache(maxsize=5)
    def info(self, __key: str) -> Union[Generator[str, any, None], list[str]]:
        if __key == TRANSLATION_ENGINE:
            return String.join(', ', self.supported_engines, max_length=250)
        elif __key in [IGNORE_LANGUAGES, TARGET_LANGUAGES]:
            return String.join(', ', self.supported_languages, max_length=250)
        return super().info(__key)

    @staticmethod
    @lru_cache(maxsize=1)
    def __supported_engines():
        return ts.translators_pool
