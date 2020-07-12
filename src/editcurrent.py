import aqt
from aqt import dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox
from aqt.utils import restoreGeom, saveGeom, tooltip
from aqt.editcurrent import EditCurrent

from os.path import  join, dirname
from aqt.utils import showText

from aqt.editor import Editor
from .editor import PersistentEditor

def get_editor_js() -> str:
    editor_js_file = join(dirname(__file__), 'editor.js')

    with open(editor_js_file, "r", encoding="utf-8") as editor_js:
        return editor_js.read() 

class PersistentEditCurrent(EditCurrent):
    def __init__(self, mw) -> None:
        QDialog.__init__(self, None, Qt.Window)
        mw.setupDialogGC(self)
        self.mw = mw
        self.form = aqt.forms.editcurrent.Ui_Dialog()
        self.form.setupUi(self)
        self.setWindowTitle(_("Persistent Edit Current")) # NOTE diverge from Anki
        self.setMinimumHeight(400)
        self.setMinimumWidth(250)
        self.form.buttonBox.button(QDialogButtonBox.Close).setShortcut(
            QKeySequence("Ctrl+Return")
        )
        self.editor = PersistentEditor(self.mw, self.form.fieldsArea, self) # NOTE diverge from Anki
        self.editor.card = self.mw.reviewer.card

        self.editor.web.eval(get_editor_js()) # NOTE diverge from Anki

        if self.mw.reviewer.state == 'question':
            self.editor.setNote(self.mw.reviewer.card.note())
            self.obscureEditor()
        else:
            self.editor.setNote(self.mw.reviewer.card.note(), focusTo=0)
            self.unobscureEditor()

        restoreGeom(self, "editcurrent")
        gui_hooks.state_did_reset.append(self.onReset)
        self.mw.requireReset()
        self.show()
        # reset focus after open, taking care not to retain webview
        # pylint: disable=unnecessary-lambda
        self.mw.progress.timer(100, lambda: self.editor.web.setFocus(), False)

    def reopen(self, mw):
        self.reject()

    def setNote(self, note):
        self.editor.setNote(note)

    def obscureEditor(self):
        self.editor.web.eval('PersistentEditor.obscure()')

    def unobscureEditor(self):
        pass

    def _saveAndClose(self) -> None:
        gui_hooks.state_did_reset.remove(self.onReset)

        self.editor.cleanup() # NOTE diverge from Anki

        saveGeom(self, "editcurrent")
        aqt.dialogs.markClosed("EditCurrent")
        QDialog.reject(self)
