from typing import Union, Literal

from aqt import dialogs, mw
from aqt.reviewer import Reviewer
from aqt.gui_hooks import reviewer_will_end, reviewer_did_answer_card, card_will_show

def get_editcurrent():
    return dialogs._dialogs['EditCurrent'][1]

def obscure_editcurrent(content, card, side: Literal['reviewAnswer', 'reviewQuestion']):
    current_editcurrent = get_editcurrent()

    if mw.reviewer.triggerObscure and current_editcurrent:
        if side == 'reviewQuestion':
            current_editcurrent.obscureEditor()
        elif side == 'reviewAnswer':
            current_editcurrent.unobscureEditor()

    mw.reviewer.triggerObscure = True

    return content

def reset_editcurrent(reviewer, card, ease):
    current_editcurrent = get_editcurrent()

    if current_editcurrent and card:
        current_editcurrent.setNote(card.note())
        current_editcurrent.obscureEditor()

def close_editcurrent():
    current_editcurrent = get_editcurrent()

    if current_editcurrent:
        current_editcurrent.saveAndClose()

def init_reviewer():
    card_will_show.append(obscure_editcurrent)

    reviewer_did_answer_card.append(reset_editcurrent)
    reviewer_will_end.append(close_editcurrent)

