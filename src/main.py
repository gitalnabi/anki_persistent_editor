from aqt import dialogs
from aqt.main import ResetReason
from aqt.editcurrent import EditCurrent
from aqt.gui_hooks import (
    main_window_should_require_reset,
    state_will_change,
)

def do_not_require_from_editcurrent(should_reset, reason, context):
    return False if (
        reason == ResetReason.EditCurrentInit or
        reason == ResetReason.EditorBridgeCmd and isinstance(context.parentWindow, EditCurrent)
    ) else should_reset

def close_editcurrent_when_leaving_review(state, oldstate):
    if (
        oldstate == 'review' and
        state in ['overview', 'deckBrowser'] and 
        (editcurrent := dialogs._dialogs['EditCurrent'][1])
    ):
        editcurrent.saveAndClose()
        dialogs.markClosed('EditCurrent')

def init_mw():
    main_window_should_require_reset.append(do_not_require_from_editcurrent)
    state_will_change.append(close_editcurrent_when_leaving_review)
