from PyQt5.QtCore import QObject, pyqtSignal
from aqt.tagedit import TagEdit

class PersistentTagEdit(TagEdit):
    gainedFocus = pyqtSignal()

    def focusInEvent(self, evt):
        super().focusInEvent(evt)
        self.gainedFocus.emit()
