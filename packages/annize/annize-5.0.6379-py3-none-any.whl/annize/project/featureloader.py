# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Feature module loader.
"""

import abc
import importlib
import sys
import threading
import typing as t


class FeatureLoader(abc.ABC):

    @abc.abstractmethod
    def load_feature(self, name: str) -> t.Optional[t.Any]:
        pass


class DefaultFeatureLoader(FeatureLoader):

    _FEATURES_NAMESPACE = "annize.features"

    def __init__(self):
        self.__cache = {}
        self.__cachelock = threading.Lock()
        for modulename in list(sys.modules.keys()):  # TODO not really a perfect solution
            if modulename.startswith(f"{self._FEATURES_NAMESPACE}."):
                sys.modules.pop(modulename)

    def load_feature(self, name):
        with self.__cachelock:
            result = self.__cache.get(name, None)
            if not result:
                try:
                    self.__cache[name] = result = importlib.import_module(f"{self._FEATURES_NAMESPACE}.{name}")
                except ImportError:
                    result = None
        if hasattr(result, "__path__"):
            result = self.load_feature(f"{name}.common")
        return result
