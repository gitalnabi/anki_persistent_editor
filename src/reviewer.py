from typing import Literal

from aqt import dialogs, mw
from aqt.main import AnkiQt
from aqt.reviewer import Reviewer
from aqt.gui_hooks import (
    card_will_show,
    webview_will_set_content,
    reviewer_did_show_question,
    reviewer_did_answer_card,
    reviewer_will_end,
)

from .editor_helper import obscure_if_question, unobscure_all
from .utils import base_path


def get_editcurrent():
    return dialogs._dialogs["EditCurrent"][1]


def obscure_editcurrent(content, card, side: Literal["reviewAnswer", "reviewQuestion"]):
    if (
        side.startswith("review")
        and (current_editcurrent := get_editcurrent())
        and (current_editor := current_editcurrent.editor)
        and current_editor.web
    ):
        if side == "reviewQuestion" and not getattr(
            mw.reviewer, "do_not_reload_editor_if_question", False
        ):
            current_note = card.note()

            if current_editor.note != current_note:
                current_editor.setNote(current_note)

            obscure_if_question(current_editor)

        elif side == "reviewAnswer":
            unobscure_all(current_editor)

        mw.reviewer.do_not_reload_editor_if_question = False

    return content


shim_show_question = """
if (!globalThis.hasOwnProperty('oldShowQuestion')) {
    globalThis.oldShowQuestion = _showQuestion
}

_showQuestion = flipShowQuestion
"""

reset_show_question = """
if (globalThis.hasOwnProperty('oldShowQuestion')) {
    _showQuestion = globalThis.oldShowQuestion
    delete globalThis.oldShowQuestion
}
"""


def setup_reviewer(web_content, context):
    if isinstance(context, Reviewer):
        web_content.js.append(f"{base_path}/reviewer.js")


def stop_fading_on_question(card):
    mw.reviewer.web.eval(shim_show_question)


def start_fading_again(reviewer, card, ease):
    reviewer.web.eval(reset_show_question)


def close_editcurrent():
    current_editcurrent = get_editcurrent()

    if current_editcurrent:
        current_editcurrent.saveAndClose()


def init_reviewer():
    card_will_show.append(obscure_editcurrent)

    webview_will_set_content.append(setup_reviewer)
    reviewer_did_show_question.append(stop_fading_on_question)
    reviewer_did_answer_card.append(start_fading_again)
    reviewer_will_end.append(close_editcurrent)
