# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
import sys
import typing as t

import annize.context
import annize.data
import annize.i18n


class UserFeedbackController:

    def message_dialog(self, message: str, answers: t.List[str], config_key: t.Optional[str]) -> int:
        raise NotImplementedError()

    def input_dialog(self, question: str, suggested_answer: str, config_key: t.Optional[str]) -> t.Optional[str]:
        raise NotImplementedError()

    def choice_dialog(self, question: str, choices: t.List[str], config_key: t.Optional[str]) -> t.Optional[int]:
        raise NotImplementedError()


class NullUserFeedbackController:

    def message_dialog(self, *_):
        raise UnsatisfiableUserFeedbackAttemptError()

    def input_dialog(self, *_):
        raise UnsatisfiableUserFeedbackAttemptError()

    def choice_dialog(self, *_):
        raise UnsatisfiableUserFeedbackAttemptError()


class UnsatisfiableUserFeedbackAttemptError(RuntimeError):

    def __init__(self):
        super().__init__("Attempted to engage in a dialog with the user in a situation that does not allow it.")


_USERFEEDBACK_CONTROLLERS = annize.data.UniqueId("userfeedback_controllers").processonly_long_str  # TODO unify such variable names


def _controllers_tuples_for_context(context: annize.context.Context) -> t.List[t.Tuple[int, UserFeedbackController]]:
    return context.object_by_name(_USERFEEDBACK_CONTROLLERS, [(-sys.maxsize, NullUserFeedbackController())],
                                  create_nonexistent=True)


def _controllers_for_context(context: annize.context.Context) -> t.List[UserFeedbackController]:
    ctlrtuples = _controllers_tuples_for_context(context)
    ctlrtuples.sort(key=lambda ctlrtuple: -ctlrtuple[0])
    return [ctlrtuple[1] for ctlrtuple in ctlrtuples]


def _add_controller_to_context(*, controller: UserFeedbackController, context: annize.context.Context,
                               priority_index: int = 0) -> None:
    _controllers_tuples_for_context(context).append((priority_index, controller))


def message_dialog(message: annize.i18n.TrStrOrStr, answers: t.Iterable[annize.i18n.TrStrOrStr], *,
                   config_key: t.Optional[str] = None) -> int:
    for controller in _controllers_for_context(annize.context.current()):
        try:
            return controller.message_dialog(str(message), [str(ans) for ans in answers], config_key)
        except UnsatisfiableUserFeedbackAttemptError:
            pass
    raise UnsatisfiableUserFeedbackAttemptError()


def input_dialog(message: annize.i18n.TrStrOrStr, *, suggested_answer: annize.i18n.TrStrOrStr,
                 config_key: t.Optional[str] = None) -> t.Optional[str]:
    for controller in _controllers_for_context(annize.context.current()):
        try:
            return controller.input_dialog(str(message), str(suggested_answer), config_key)
        except UnsatisfiableUserFeedbackAttemptError:
            pass
    raise UnsatisfiableUserFeedbackAttemptError()


def choice_dialog(message: annize.i18n.TrStrOrStr, choices: t.Iterable[annize.i18n.TrStrOrStr], *,
                  config_key: t.Optional[str] = None) -> t.Optional[int]:
    for controller in _controllers_for_context(annize.context.current()):
        try:
            return controller.choice_dialog(str(message), [str(choice) for choice in choices], config_key)
        except UnsatisfiableUserFeedbackAttemptError:
            pass
    raise UnsatisfiableUserFeedbackAttemptError()
