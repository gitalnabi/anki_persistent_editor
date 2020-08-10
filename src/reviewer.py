from typing import Union, Literal

from aqt import dialogs, mw
from aqt.reviewer import Reviewer
from aqt.gui_hooks import (
    reviewer_will_end,
    reviewer_did_answer_card,
    reviewer_did_show_question,
    card_will_show,
    webview_will_set_content,
)

def toggle_reviewer(reviewer):
    state = reviewer.state

    if state == 'question':
        reviewer._getTypedAnswer()

    elif state == 'answer':
        reviewer._showQuestion()

def refresh_reviewer(reviewer):
    state = reviewer.state

    if state == 'question':
        reviewer._showQuestion()

    elif state == 'answer':
        reviewer._getTypedAnswer()

def redraw_reviewer(reviewer):
    # Maybe reviewer already finished
    if reviewer.card is None:
        return

    # Trigger redrawing of mw without losing focus
    reviewer.card.load()
    reviewer.triggerObscure = False

    refresh_reviewer(reviewer)

def get_editcurrent():
    return dialogs._dialogs['EditCurrent'][1]

def obscure_editcurrent(content, card, side: Literal['reviewAnswer', 'reviewQuestion']):
    if side.startswith('review'):
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

def stop_fading_on_question(card):
    mw.reviewer.web.eval('qFade = 0')

def start_fading_again(reviewer, card, ease):
    reviewer.web.eval('qFade = 100')

def init_reviewer():
    card_will_show.append(obscure_editcurrent)
    reviewer_will_end.append(close_editcurrent)
    webview_will_set_content.append(setup_reviewer)

    reviewer_did_show_question.append(stop_fading_on_question)
    reviewer_did_answer_card.append(start_fading_again)
