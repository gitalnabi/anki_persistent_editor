from aqt import QDialog, QLayout, QKeySequence

from .forms.settings_ui import Ui_Settings


class Settings(QDialog):
    def __init__(self, mw, callback):
        super().__init__(parent=mw)

        self.mw = mw

        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        self.cb = callback

        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def setupUi(
        self, flip_shortcut: str, presentation_mode: bool, presentation_shortcut: str
    ):
        self.ui.flipShortcut.setKeySequence(QKeySequence(flip_shortcut))

        self.ui.presentationCheckBox.setChecked(presentation_mode)
        self.ui.presentationShortcut.setKeySequence(QKeySequence(presentation_shortcut))

    def accept(self):
        flip_shortcut = self.ui.flipShortcut.keySequence().toString()

        presentation_mode = self.ui.presentationCheckBox.isChecked()
        presentation_shortcut = self.ui.presentationShortcut.keySequence().toString()

        self.cb(flip_shortcut, presentation_mode, presentation_shortcut)
        super().accept()
