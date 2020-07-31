from typing import Union, Literal

from aqt import dialogs, mw
from aqt.reviewer import Reviewer
from aqt.gui_hooks import (
    reviewer_will_end,
    reviewer_did_answer_card,
    card_will_show,
    webview_will_set_content,
)

def toggle_reviewer(reviewer):
    state = reviewer.state

    if state == 'question':
        reviewer._getTypedAnswer()

    elif state == 'answer':
        reviewer._showQuestion()

def get_editcurrent():
    return dialogs._dialogs['EditCurrent'][1]

def obscure_editcurrent(content, card, side: Literal['reviewAnswer', 'reviewQuestion']):
    current_editcurrent = get_editcurrent()

    if mw.reviewer.triggerObscure and current_editcurrent:
        if side == 'reviewQuestion':
            current_note = card.note()

            if current_editcurrent.editor.note != current_note:
                current_editcurrent.setNote(current_note)

            current_editcurrent.obscureEditor()

        elif side == 'reviewAnswer':
            current_editcurrent.unobscureEditor()

    mw.reviewer.triggerObscure = True

    return content

def close_editcurrent():
    current_editcurrent = get_editcurrent()

    if current_editcurrent:
        current_editcurrent.saveAndClose()

def setup_reviewer(web_content, context):
    if isinstance(context, Reviewer):
        context.triggerObscure = True

def init_reviewer():
    card_will_show.append(obscure_editcurrent)
    reviewer_will_end.append(close_editcurrent)

    webview_will_set_content.append(setup_reviewer)
