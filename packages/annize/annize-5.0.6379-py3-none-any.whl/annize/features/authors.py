# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.context


class Author:

    def __init__(self, *, fullname: str, email: str = None):
        self.__fullname = fullname
        self.__email = email

    @property
    def fullname(self) -> str:
        return self.__fullname

    @property
    def email(self) -> t.Optional[str]:
        return self.__email


def default_project_authors() -> t.List[Author]:
    return annize.context.objects_by_type(Author)
