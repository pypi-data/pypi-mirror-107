# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.callconv
import annize.i18n


class Kind:

    @annize.callconv.parameter_from_childnodes("flags")
    def __init__(self, *, label: str, importance: int, flags: t.List[object] = None):
        self.__label = label
        self.__importance = importance
        self.__flags = flags or []

    @property
    def label(self) -> str:
        return annize.i18n.tr_if_trstr(self.__label)

    @property
    def importance(self) -> int:
        return self.__importance

    @property
    def flags(self) -> t.List[object]:
        return list(self.__flags)


class Dependency:

    @annize.callconv.parameter_from_childnodes("kind")
    def __init__(self, *, kind: Kind = None, label: str = None, comment: str = None, icon: str = None,
                 importance: int = 0):
        # TODO noh  t.Optional[...]
        self.__kind = kind or Required()
        self.__label = label
        self.__comment = comment
        self.__icon = icon
        self.__importance = importance

    @property
    def kind(self) -> Kind:
        return self.__kind

    @property
    def label(self) -> str:
        return self.__label

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def icon(self) -> str:
        return self.__icon

    @property
    def importance(self) -> int:
        return self.__importance


class Required(Kind):

    def __init__(self, **b):
        super().__init__(label=annize.i18n.TrStr.tr("an_Dep_Required"), importance=0, **b)


class Recommended(Kind):

    def __init__(self, **b):
        super().__init__(label=annize.i18n.TrStr.tr("an_Dep_Recommended"), importance=-200_000, **b)


class Included(Kind):

    def __init__(self, **b):
        super().__init__(label=annize.i18n.TrStr.tr("an_Dep_Included"), importance=-400_000, **b)


class GnuLinux(Dependency):

    @annize.callconv.parameter_from_childnodes("kind")
    def __init__(self, *, kind=None, comment=""):
        super().__init__(kind=kind, label="GNU/Linux", icon="linux", comment=comment)


class Artwork(Dependency):  # pylint: disable=redefined-builtin

    @annize.callconv.parameter_from_childnodes("kind")
    def __init__(self, *, kind=None, label, origin: str = None, comment: str = None, license: str = None):
        fullcomment = []
        if comment:
            fullcomment.append(comment)
        if license:
            fullcomment.append(f"License: {license}")
        if origin:
            fullcomment.append(f"`from here <{origin}>`__")
        super().__init__(kind=kind, label=label, icon="artwork", comment="; ".join(fullcomment))


def dependencies_to_rst_text(dependencies: t.List[Dependency]) -> str:
    content = ""
    dependencies = sorted(dependencies, key=lambda dep: (-dep.kind.importance, -dep.importance, type(dep).__name__,
                                                         dep.icon or "~", dep.label))
    for dependency in dependencies:
        if not dependency.label:
            continue
        icon = dependency.icon or "misc"
        comment = f" ({dependency.comment})" if dependency.comment else ""
        label = dependency.label.replace("`", "'")
        kind = dependency.kind.label
        dlm = ": " if (len(comment) > 0) else ""
        content += f"\n|annizeicon_{icon}| {kind}: **{label}**{comment}\n\n"
    return content
