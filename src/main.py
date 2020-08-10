from aqt import mw
from aqt.main import AnkiQt
from aqt.editcurrent import EditCurrent

from anki.hooks import wrap

def do_not_require_from_editcurrent(self, _old):
    active_window = mw.app.activeWindow()

    if ((isinstance(active_window, AnkiQt) and mw.state == 'review') or
            isinstance(active_window, EditCurrent)):
        return False

    return _old()

def init_mw():
    AnkiQt.interactiveState = wrap(AnkiQt.interactiveState, do_not_require_from_editcurrent, pos='around')
