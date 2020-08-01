from aqt import dialogs, mw
from aqt.main import AnkiQt
from anki.hooks import wrap

# https://stackoverflow.com/questions/1443129/completely-wrap-an-object-in-python
class AvoidRequireReset(AnkiQt):
    def __init__(self, baseObject):
        self.__class__ = type(
            baseObject.__class__.__name__,
            (self.__class__, baseObject.__class__),
            {},
        )
        self.__dict__ = baseObject.__dict__

    def requireReset(self, modal=False):
        pass

def on_persistent_edit_current(mw, _old):
    dialogs.open("EditCurrent", AvoidRequireReset(mw))

def init_mw():
    AnkiQt.onEditCurrent = wrap(AnkiQt.onEditCurrent, on_persistent_edit_current, 'around')
