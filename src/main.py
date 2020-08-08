from aqt import mw
from aqt.main import AnkiQt
from aqt.editcurrent import EditCurrent

from anki.hooks import wrap

def do_not_require_reset(interactive_state):
    active_window = mw.app.activeWindow()

    if isinstance(active_window, EditCurrent) or (isinstance(active_window, AnkiQt) and mw.state == 'review'):
        return False

    return interactive_state 

def require_reset(self, modal=False, _old=None):
    "Signal queue needs to be rebuilt when edits are finished or by user."
    self.autosave()
    self.resetModal = modal

    if do_not_require_reset(self.interactiveState()):
        self.moveToState("resetRequired")

def init_mw():
    AnkiQt.requireReset = wrap(AnkiQt.requireReset, require_reset, pos='around')
