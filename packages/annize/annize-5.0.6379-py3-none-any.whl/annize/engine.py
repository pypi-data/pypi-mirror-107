# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.context
import annize.fs
import annize.i18n
import annize.project.materializer
import annize.userfeedback


class LoadedProject:

    def __init__(self, context: annize.context.Context, null_culture: annize.i18n.Culture):
        self.__context = context
        self.__null_culture = null_culture

    def __enter__(self):
        self.__context.__enter__()
        self.__null_culture.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__null_culture.__exit__(exc_type, exc_val, exc_tb)
        self.__context.__exit__(exc_type, exc_val, exc_tb)

    @property
    def context(self) -> annize.context.Context:
        return self.__context


def load_project_definition(projectdefinition: annize.project.ProjectDefinition, *,
                            annize_config_rootpath: str) -> LoadedProject:
    with LoadedProject(annize.context.Context(), annize.i18n.get_culture("en")) as loaded_project:  # TODO better null_culture
        annize.project.materializer.materialize(nodes=projectdefinition.nodes)
        _prepare_context(loaded_project.context, annize_config_rootpath=annize_config_rootpath)
        return loaded_project


def load_project(project_path: str) -> LoadedProject:
    annize_config_root_file = find_project_annize_config_root_file(project_path)
    projectdefinition = annize.project.ProjectDefinition.from_files(annize_config_root_file)
    return load_project_definition(projectdefinition, annize_config_rootpath=annize_config_root_file)


def find_project_annize_config_root_file(project_path: str) -> t.Optional[str]:
    currfs = annize.fs.fsentry_by_path(project_path)
    if currfs and currfs.is_file():  # TODO noh resolve symlinks?!
        return currfs.readable_path()
    while currfs and currfs.exists():
        for potrespath in ["", *_metanames]:
            fpotresfs = currfs.child_by_relative_path(potrespath).child_by_relative_path("project.xml")
            if fpotresfs.is_file():  # TODO noh resolve symlinks?!
                return fpotresfs.readable_path()
        currfs = currfs.parent()
    return None


def guess_project_root_directory(annize_config_rootpath: str) -> str:
    result = annize.fs.fsentry_by_path(annize_config_rootpath).parent()
    if result.basename() in _metanames:
        result = result.parent()
    return result.readable_path()


def _prepare_context(context: annize.context.Context, *, annize_config_rootpath: str) -> None:
    import annize.features.base  # TODO dangerous to import features inside engine (see our feature import machinery)?! (but maybe okay inside a function?!)
    context.set_object_name(annize_config_rootpath, annize.features.base._ANNIZE_CONFIG_ROOTPATH)
    import annize.userfeedback.tty#TODO
    annize.userfeedback._add_controller_to_context(controller=annize.userfeedback.tty.TtyUserFeedbackController(),
                                                   context=context)


_metanames = ["meta", ".meta", "-meta", "_meta", "!meta", "~meta", "$meta"]
