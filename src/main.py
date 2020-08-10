from aqt import mw, dialogs
from aqt.main import AnkiQt
from aqt.editcurrent import EditCurrent
from aqt.gui_hooks import state_will_change

from anki.hooks import wrap

def do_not_require_from_editcurrent(self, _old):
    active_window = mw.app.activeWindow()

    if ((isinstance(active_window, AnkiQt) and mw.state == 'review') or
            isinstance(active_window, EditCurrent)):
        return False

    return _old(self)

def close_editcurrent_when_leaving_review(state, oldstate):
    if (
        oldstate == 'review' and
        state in ['overview', 'deckBrowser'] and 
        (editcurrent := dialogs._dialogs['EditCurrent'][1])
    ):
        editcurrent.saveAndClose()
        dialogs.markClosed('EditCurrent')

def init_mw():
    AnkiQt.interactiveState = wrap(AnkiQt.interactiveState, do_not_require_from_editcurrent, pos='around')
    state_will_change.append(close_editcurrent_when_leaving_review)
