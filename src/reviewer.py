from typing import Literal

from aqt import dialogs, mw
from aqt.reviewer import Reviewer
from aqt.gui_hooks import (
    card_will_show,
    webview_will_set_content,
    reviewer_did_show_question,
    reviewer_did_answer_card,
    reviewer_will_end,
)

from .editor_helper import maybe_obscure_all, unobscure_all

def get_editcurrent():
    return dialogs._dialogs['EditCurrent'][1]

def obscure_editcurrent(content, card, side: Literal['reviewAnswer', 'reviewQuestion']):
    if side.startswith('review'):
        current_editcurrent = get_editcurrent()

        if mw.reviewer.trigger_obscure and current_editcurrent:
            current_editor = current_editcurrent.editor

            if side == 'reviewQuestion':
                current_note = card.note()

                if current_editor.note != current_note:
                    current_editor.setNote(current_note)

                maybe_obscure_all(current_editor)

            elif side == 'reviewAnswer':
                unobscure_all(current_editor)

        mw.reviewer.trigger_obscure = True

    return content

def setup_reviewer(web_content, context):
    # only set on first init of reviewer, not on reset
    if isinstance(context, Reviewer) and not hasattr(context, 'trigger_obscure'):
        context.trigger_obscure = True

def stop_fading_on_question(card):
    mw.reviewer.web.eval('qFade = 0')

def start_fading_again(reviewer, card, ease):
    reviewer.web.eval('qFade = 100')

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
