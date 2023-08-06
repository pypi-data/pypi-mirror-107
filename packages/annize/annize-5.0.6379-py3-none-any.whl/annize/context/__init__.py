# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import threading

import annize.data


_T = t.TypeVar("_T")


class Context:

    _METADATA_IS_TOPLEVEL_OBJECT = annize.data.UniqueId("is_toplevel_object").processonly_long_str

    def __init__(self):
        self.__lock = threading.RLock()
        self.__objectsdict = {}
        self.__objectnames = {}
        self.__objectmetadata = {}

    def object_by_name(self, name: str, defaultvalue: t.Optional[t.Any] = None, *,
                       create_nonexistent: bool = False) -> t.Optional[t.Any]:
        with self.__lock:
            result = self.__objectsdict.get(name, self)
            if result == self:
                result = defaultvalue
                if create_nonexistent:
                    self.set_object_name(result, name)
            return result

    def object_names(self, obj: t.Any) -> t.List[str]:
        with self.__lock:
            self.__object_raw_name(obj)
            return self.__objectnames[id(obj)]

    def __put_object(self, name: str, obj: t.Any) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not name:
            raise ValueError("name must not be empty")
        with self.__lock:
            if self.__objectsdict.get(name, obj) != obj:
                raise ValueError(f"name '{name}' already assigned")
            self.__objectsdict[name] = obj
            onames = self.__objectnames[id(obj)] = self.__objectnames.get(id(obj), [])
            onames.append(name)

    def __object_raw_name(self, obj: t.Any) -> str:
        names = self.__objectnames.get(id(obj), ())
        rawnames = [name for name in names if not self.is_friendly_name(name)]
        if rawnames:
            return rawnames[-1]
        rawname = annize.data.UniqueId(str(id(obj))).long_str
        self.__put_object(rawname, obj)
        return rawname

    def object_name(self, obj: t.Any) -> str:
        names = self.object_names(obj)
        friendlynames = [name for name in names if self.is_friendly_name(name)]
        return friendlynames[0] if friendlynames else names[0]

    def set_object_name(self, obj: t.Any, name: str) -> None:
        self.__put_object(name, obj)

    def objects_by_type(self, objtype: t.Type[_T], toplevel_only: bool = True) -> t.List[_T]:
        with self.__lock:
            result = []
            for obj in self.__objectsdict.values():
                if isinstance(obj, objtype) and obj not in result:
                    result.append(obj)
        if toplevel_only:
            result = [obj for obj in result if self.is_toplevel_object(obj)]
        return result

    def add_object(self, obj: t.Any) -> str:
        return self.object_name(obj)

    def is_friendly_name(self, name: str) -> bool:
        return not name.startswith(annize.data.UniqueId("").processonly_long_str)

    def is_toplevel_object(self, obj: t.Any) -> bool:
        return self.get_object_metadata(obj, self._METADATA_IS_TOPLEVEL_OBJECT, False)

    def mark_object_as_toplevel(self, obj: t.Any) -> None:
        self.add_object(obj)
        return self.set_object_metadata(obj, self._METADATA_IS_TOPLEVEL_OBJECT, True)

    # TODO use object metadata for names as well

    def get_object_metadata(self, obj: t.Any, key: str, defaultvalue: t.Optional[t.Any] = None) -> t.Optional[t.Any]:
        return self.__object_metadata_dict(obj).get(key, defaultvalue)

    def set_object_metadata(self, obj: t.Any, key: str, value: t.Optional[t.Any] = None) -> None:
        self.__object_metadata_dict(obj)[key] = value

    def __object_metadata_dict(self, obj: t.Any) -> t.Dict[str, t.Optional[t.Any]]:
        result = self.__objectmetadata[id(obj)] = self.__objectmetadata.get(id(obj), {})
        return result

    def __enter__(self):
        _contextsstack.stack = stack = getattr(_contextsstack, "stack", [])
        stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _contextsstack.stack.pop()

# TODO xx xy noh global variables?!


_contextsstack = threading.local()


def current() -> Context:
    stack = getattr(_contextsstack, "stack", None)
    if not stack:
        raise OutOfContextError()
    return stack[-1]


class OutOfContextError(TypeError):

    def __init__(self):
        super().__init__("There is no current Annize context")


def object_by_name(name: str, defaultvalue: t.Optional[t.Any] = None, *,
                   create_nonexistent: bool = False) -> t.Optional[t.Any]:
    return current().object_by_name(name, defaultvalue, create_nonexistent=create_nonexistent)


def object_names(obj: t.Any) -> t.List[str]:
    return current().object_names(obj)


def object_name(obj: t.Any) -> str:
    return current().object_name(obj)


def set_object_name(obj: t.Any, name: str) -> None:
    current().set_object_name(obj, name)


def objects_by_type(objtype: t.Type[_T], toplevel_only: bool = True) -> t.List[_T]:
    return current().objects_by_type(objtype, toplevel_only=toplevel_only)


def add_object(obj: t.Any) -> str:
    return current().add_object(obj)


def is_friendly_name(name: str) -> bool:
    return current().is_friendly_name(name)


def is_toplevel_object(obj: t.Any) -> bool:
    return current().is_toplevel_object(obj)


def get_object_metadata(obj: t.Any, key: str, defaultvalue: t.Optional[t.Any] = None) -> t.Optional[t.Any]:
    return current().get_object_metadata(obj, key, defaultvalue)


def set_object_metadata(obj: t.Any, key: str, value: t.Optional[t.Any] = None) -> None:
    return current().set_object_metadata(obj, key, value)


# TODO xx xy how to cleanup whenever materializer loads features? contextvars?
