# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.userfeedback


class TtyUserFeedbackController(annize.userfeedback.UserFeedbackController):

    def __dialog_frame_message(self, message: str) -> str:
        return f"--------------------------------------------------------------------------------\n{message}\n"  # TODO

    def __dialog_frame_configkey(self, config_key: str) -> str:
        return f"\n(This answer could also be automated by key '{config_key}')\n" if config_key else ""  # TODO i18n

    def __dialog_frame_actions(self, text: str) -> str:
        return f"--------------------------------------------------------------------------------\n{text}"  # TODO

    def __action_line(self, num: t.Any, text: str) -> str:
        return f"{str(num).rjust(5, ' ')} : {text}\n"

    def __dialog(self, message: str, config_key: str, actionstext: str) -> str:
        if False:  # TODO check terminal available
            raise annize.userfeedback.UnsatisfiableUserFeedbackAttemptError()
        print(self.__dialog_frame_message(message)
              + self.__dialog_frame_configkey(config_key)
              + self.__dialog_frame_actions(actionstext))
        return input(">>> ")

    def message_dialog(self, message, answers, config_key):
        actionstext = "Please enter the number for your answer.\n\n"  #TODO i18n
        for ianswer, answer in enumerate(answers):
            actionstext += self.__action_line(ianswer, answer)
        while True:
            answer = self.__dialog(message, config_key, actionstext)
            try:
                answer = int(answer)
            except ValueError:
                continue
            if 0 <= answer < len(answers):
                return answer

    def input_dialog(self, question, suggested_answer, config_key):
        actionstext = (f"Please enter your answer.\n"
                       f"You can also enter '---' for cancelling or '!!!' for accepting\n"
                       f"the suggested answer '{suggested_answer}'.\n\n")  #TODO i18n
        answer = self.__dialog(question, config_key, actionstext)
        if answer == "---":
            return None
        if answer == "!!!":
            return suggested_answer
        return answer

    def choice_dialog(self, question, choices, config_key):
        actionstext = "Please enter the number for your choice.\n\n"  #TODO i18n
        for ianswer, answer in enumerate(choices):
            actionstext += self.__action_line(ianswer, answer)
        actionstext += self.__action_line(-1, "Cancel")  # TODO i18n
        actionstext += self.__action_line(-1, "Cancel")  # TODO i18n
        while True:
            answer = self.__dialog(question, config_key, actionstext)
            try:
                answer = int(answer)
            except ValueError:
                continue
            if answer == -1:
                return None
            if 0 <= answer < len(choices):
                return answer
