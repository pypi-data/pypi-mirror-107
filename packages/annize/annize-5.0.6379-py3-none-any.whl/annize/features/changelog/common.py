# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import datetime
import typing as t

import annize.callconv
import annize.context
import annize.data
import annize.i18n
import annize.features.versioncontrol.common
import annize.features.version


class Item:

    @annize.callconv.parameter_from_childnodes("text")
    def __init__(self, *, text: annize.i18n.TrStr):  # TODO "text" typehint weird
        self.__text = text

    @property
    def text(self):
        return self.__text


def _items_matcher(o):  #TODO
    return isinstance(o, annize.i18n.TrStr) or isinstance(o, str) or isinstance(o, Item)


class Entry:  # TODO

    @annize.callconv.parameter_from_childnodes("version")
    @annize.callconv.parameter_from_childnodes("time")
    @annize.callconv.parameter_from_childnodes("items", if_passing=_items_matcher, if_typehint_matches=False)  # TODO
    def __init__(self, *, version: annize.data.Version = None, time: datetime.datetime = None,
                 items: t.Iterable[Item]):  # TODO t.Optional[annize.data.Version], time: t.Optional[datetime.datetime],
        self.__version = version
        self.__time = time
        self.__items = []
        for item in items:
            self.__items.append(item if isinstance(item, Item) else Item(text=item))

    @property
    def items(self) -> t.List[Item]:
        return self.__items

    @property
    def time(self) -> t.Optional[datetime.datetime]:
        return self.__time

    @property
    def version(self) -> t.Optional[annize.data.Version]:
        return self.__version


class Changelog:

    @annize.callconv.parameter_from_childnodes("entries")
    def __init__(self, *, entries: t.Iterable[Entry] = ()):
        self.__entries = list(entries)

    @property
    def entries(self) -> t.List[Entry]:
        return self.__entries


class ByVersionControlSystemCommitMessagesChangelog(Changelog):  # TODO weg later?!

    _S_CHANGE = "##CHANGE:"
    _S_LABEL = "##LABEL:"

    def __init__(self):
        super().__init__()

    # TODO i18n of changelog items ?!
    @property
    def entries(self):
        entries = []
        vcs = annize.features.versioncontrol.common.default_version_control_system()
        if vcs:
            items = []
            for revision in vcs.get_revision_list():
                commitmsg = vcs.get_commit_message(revision)
                for commitmsgline in [x.strip() for x in commitmsg.split("\n")]:
                    if commitmsgline.startswith(self._S_CHANGE):
                        items.append(Item(text=commitmsgline[len(self._S_CHANGE):].strip()))
                    elif commitmsgline.startswith(self._S_LABEL):
                        if len(items) > 0:
                            version = annize.data.Version(text=commitmsgline[len(self._S_LABEL):].strip(),
                                                          pattern=annize.features.version.default_version_pattern())#TODO pattern
                            time = vcs.get_commit_time(revision)
                            entries.append(Entry(version=version, time=time, items=reversed(items)))
                            items = []
        return entries


def default_changelog() -> Changelog:
    prvs = annize.context.objects_by_type(Changelog, toplevel_only=True)
    if len(prvs) > 1:
        raise Exception("TODO")
    if len(prvs) == 1:
        return prvs[0]
    return ByVersionControlSystemCommitMessagesChangelog()
