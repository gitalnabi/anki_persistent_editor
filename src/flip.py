from aqt import mw
from aqt.gui_hooks import state_shortcuts_will_change

from .reviewer_helper import toggle_reviewer
from .utils import flip_keyword


def add_flip_card(state, shortcuts):
    if state == "review":
        flip_shortcut = mw.pm.profile.get(flip_keyword, "C")
        shortcuts.append((flip_shortcut, lambda: toggle_reviewer(mw.reviewer)))


def init_flip_shortcut():
    state_shortcuts_will_change.append(add_flip_card)
