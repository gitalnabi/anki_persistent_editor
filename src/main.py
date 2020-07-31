from aqt import AnkiQt, dialogs, mw

class AvoidRequireReset:
    def __init__(self, obj):
        self.orig = obj

    def __getattr__(self, attr):
        if attr == 'requireReset':
            return lambda _self = None, _modal = None: None
        else:
            return getattr(self.orig, attr)

def init_mw():
    def onPersistentEditCurrent(self):
        dialogs.open("EditCurrent", AvoidRequireReset(self))

    # reassign method on this mw object only
    mw.onEditCurrent = onPersistentEditCurrent.__get__(mw, AnkiQt)
