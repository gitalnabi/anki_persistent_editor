from aqt import mw
from aqt.main import AnkiQt
from aqt.editcurrent import EditCurrent

from anki.hooks import wrap

def do_not_require_from_editcurrent(self, _old):
    active_window = mw.app.activeWindow()

    if ((isinstance(active_window, AnkiQt) and mw.state == 'review') or
            isinstance(active_window, EditCurrent)):
        return False

    return _old(self)

def persistent_review_state(self, oldstate, _old):
    if oldstate == 'persistentReview':
        self.reviewer.trigger_obscure = False

    _old(self, oldstate)

def init_mw():
    AnkiQt.interactiveState = wrap(AnkiQt.interactiveState, do_not_require_from_editcurrent, pos='around')
    AnkiQt._reviewState = wrap(AnkiQt._reviewState, persistent_review_state, pos='around')
