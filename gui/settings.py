from aqt import QDialog, QLayout

from .forms.settings_ui import Ui_Settings

class Settings(QDialog):
    def __init__(self, mw, callback):
        super().__init__(parent=mw)

        self.mw = mw

        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        self.cb = callback

        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def setupUi(self, flip_shortcut: str):
        self.ui.flipShortcut.setText(flip_shortcut)

    def accept(self):
        flip_shortcut = self.ui.flipShortcut.text()

        self.cb(flip_shortcut)
        super().accept()
