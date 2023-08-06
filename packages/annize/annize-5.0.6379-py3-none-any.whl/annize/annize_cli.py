#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import argparse
import json
import os
import sys
import typing as t

try:  # weird, but useful in some cases ;)
    if "__main__" == __name__:
        import annize
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.realpath(__file__)+"/../.."))

import annize.context
import annize.engine
import annize.i18n
import annize.project.materializer
import annize.userfeedback.static


def get_parser() -> argparse.ArgumentParser:
    with annize.i18n.annize_user_interaction_culture():
        parser = argparse.ArgumentParser()
        #TODO i18n !?
        parser.add_argument("--project", type=str, help=annize.i18n.tr("an_Cli_project"))
        subparsers_command = parser.add_subparsers(help=annize.i18n.tr("an_Cli_command"), required=True, dest="command")
        subparser_command_do = subparsers_command.add_parser("do", help=annize.i18n.tr("an_Cli_do"))
        subparser_command_do.add_argument("--with-answers-from-json-file", type=str, action="append", default=[],# TODO multiple times
                                          help=annize.i18n.tr("an_Cli_withAnswersFromJsonFile"))
        subparser_command_do.add_argument("--with-answers-from-json-string", type=str, action="append", default=[],# TODO multiple times
                                          help=annize.i18n.tr("an_Cli_withAnswersFromJsonString"))
        subparser_command_do.add_argument("--with-answer", type=str, action="append", nargs=2, default=[], # TODO multiple times # TODO two args
                                          help=annize.i18n.tr("an_Cli_withAnswer"))
        subparser_command_do.add_argument("taskname", default="taskchooser", type=str,
                                          help=annize.i18n.tr("an_Cli_taskname"), nargs="?")
        return parser


class Cli:

    project_default = os.getcwd()

    @classmethod
    def __answers_from_json_files(cls, destination: t.Dict, with_answers_from_json_files: t.Iterable[str]):
        for with_answers_from_json_file in with_answers_from_json_files:
            with open(with_answers_from_json_file, "r") as f:
                json_string = f.read()
            cls.__answers_from_json_strings(destination, [json_string])

    @classmethod
    def __answers_from_json_strings(cls, destination: t.Dict, with_answers_from_json_strings: t.Iterable[str]):
        for with_answers_from_json_string in with_answers_from_json_strings:
            cls.__answers_from_single_answers(destination, json.loads(with_answers_from_json_string).items())

    @classmethod
    def __answers_from_single_answers(cls, destination: t.Dict, with_answers: t.Iterable[t.Tuple[str, str]]):
        for answerkey, answervalue in with_answers:
            destination[answerkey] = answervalue

    @classmethod
    def do(cls, project: str, taskname: str, with_answers_from_json_file: t.Iterable[str],
           with_answers_from_json_string: t.Iterable[str], with_answer: t.Iterable[t.Tuple[str, str]], **_):
        with annize.engine.load_project(project or Cli.project_default) as loaded_project:
            answers = {}
            cls.__answers_from_json_files(answers, with_answers_from_json_file)
            cls.__answers_from_json_strings(answers, with_answers_from_json_string)
            cls.__answers_from_single_answers(answers, with_answer)
            for answerkey, answervalue in with_answer:
                answers[answerkey] = answervalue
            annize.userfeedback._add_controller_to_context(
                controller=annize.userfeedback.static.StaticUserFeedbackController(answers),
                context=loaded_project.context, priority_index=100_000)
            task = loaded_project.context.object_by_name(taskname)
            if not task:
                raise Exception("TODO")
            task()


def main():
    # TODO logging.basicConfig(level=logging.DEBUG)
    parser = get_parser()
    args = parser.parse_args()
    command = getattr(Cli, args.command)
    command(**args.__dict__)


if __name__ == "__main__":
    main()
