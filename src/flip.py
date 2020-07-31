from aqt import mw
from aqt.gui_hooks import state_shortcuts_will_change

def flip_card():
    if mw.reviewer.state == 'question':
        mw.reviewer._showAnswer()

    elif mw.reviewer.state == 'answer':
        mw.reviewer._showQuestion()

def add_flip_card(state, shortcuts):
    if state == 'review':
        shortcuts.append(("c", flip_card))

def init_flip_shortcut():
    state_shortcuts_will_change.append(add_flip_card)
