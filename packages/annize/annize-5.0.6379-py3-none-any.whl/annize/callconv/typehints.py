# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import importlib
import sys
import typing as t


class TypeInfo:

    def __init__(self, name: str, resolvedtype: t.Type, constructfromstringfct: t.Optional[t.Callable[[str], t.Any]]):
        self.__name = name
        self.__resolvedtype = resolvedtype
        self.__constructfromstringfct = constructfromstringfct

    @property
    def name(self) -> str:
        return self.__name

    @property
    def resolved_type(self) -> t.Type:
        return self.__resolvedtype

    @property
    def is_constructable_from_string(self) -> bool:
        return self.__constructfromstringfct is not None

    def construct_from_string(self, strvalue: str) -> t.Any:
        return self.__constructfromstringfct(strvalue)


class ListTypeInfo(TypeInfo):

    def __init__(self, name: str, innertypeinfo):
        super().__init__(name, list, None)
        self.__inner = innertypeinfo

    @property
    def inner(self) -> TypeInfo:
        return self.__inner


def get_typeinfo(for_type) -> TypeInfo:
    if isinstance(for_type, t._GenericAlias):
        # TODO runtime check: is it an Optional or List?
        return ListTypeInfo(str(for_type), get_typeinfo(for_type=for_type.__args__[0]))
    if isinstance(for_type, t.ForwardRef):
        for_type = for_type.__forward_arg__
    if isinstance(for_type, str):
        def findmodule(typename):
            for i in reversed(range(len(typename))):
                if typename[i] == ".":
                    modulename = typename[:i]
                    importlib.import_module(modulename)
                    if modulename in sys.modules:
                        return sys.modules[modulename], typename[i + 1:]
            return None, None
        containingmodule, shorttypename = findmodule(for_type)
        if shorttypename:
            for_type = eval(shorttypename, containingmodule.__dict__)  # pylint: disable=eval-used
        constructfromstringfct = None
    else:
        constructfromstringfct = for_type
    return TypeInfo(for_type.__name__, for_type, constructfromstringfct)


def get_arguments_infos(*, for_callable: t.Callable) -> t.Dict[str, TypeInfo]:
    result = {}
    mro = for_callable.mro() if isinstance(for_callable, type) else [for_callable]
    for supertype in mro:
        supertypeconstructor = getattr(supertype, "__init__", supertype)
        for paramname, paramtype in getattr(supertypeconstructor, "__annotations__", {}).items():
            result[paramname] = get_typeinfo(for_type=paramtype)
    return result
