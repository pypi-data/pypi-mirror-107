# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.callconv
import annize.context
import annize.data


class Line:

    @annize.callconv.parameter_from_childnodes("version")
    def __init__(self, *, version: annize.data.Version):
        self.__version = version

    @property
    def version(self) -> annize.data.Version:
        return self.__version


class Version(annize.data.Version):

    @annize.callconv.parameter_from_childnodes("pattern")
    def __init__(self, *, text: str = None, pattern: annize.data.version.VersionPattern = None, **segment_values):
        super().__init__(text=text, pattern=pattern or default_version_pattern(), **segment_values)


_DEFAULT_VERSION_PATTERN = annize.data.UniqueId("default_version_pattern").processonly_long_str  # TODO unify such variable names


def default_version_pattern() -> annize.data.version.VersionPattern:
    return annize.context.object_by_name(_DEFAULT_VERSION_PATTERN) or CommonVersionPattern()


def project_versions() -> t.List[annize.data.Version]:
    return annize.context.objects_by_type(annize.data.Version)


class CommonVersionPattern(annize.data.version.VersionPattern):

    def __init__(self):
        super().__init__(segments=[
            annize.data.version.NumericVersionPatternSegment(partname="major"),
            annize.data.version.SeparatorVersionPatternSegment(text="."),
            annize.data.version.NumericVersionPatternSegment(partname="minor"),
            annize.data.version.OptionalVersionPatternSegment(segments=[
                annize.data.version.SeparatorVersionPatternSegment(text="."),
                annize.data.version.NumericVersionPatternSegment(partname="build")
            ])
        ])
