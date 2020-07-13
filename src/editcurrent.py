import aqt
from aqt import dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox, QEvent
from aqt.utils import restoreGeom, saveGeom, showText
from aqt.editcurrent import EditCurrent

from os.path import  join, dirname

from .editor import PersistentEditor

def get_editor_js() -> str:
    editor_js_file = join(dirname(__file__), 'editor.js')

    with open(editor_js_file, "r", encoding="utf-8") as editor_js:
        return editor_js.read()

EDITOR_JS = get_editor_js()
EDITOR_CSS = '''
#fields td {
    position: relative;
}

.coverup {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;

    background: lavender;
    border: 1px darkgrey solid;
}
'''

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

        # NOTE diverge from Anki
        self.editor.web.eval(EDITOR_JS)
        self.editor.web.eval(f'PersistentEditor.appendStyleTag(`{EDITOR_CSS}`)')

        if self.mw.reviewer.state == 'question':
            self.editor.setNote(self.mw.reviewer.card.note())
            self.obscureEditor()
        else:
            self.editor.setNote(self.mw.reviewer.card.note(), focusTo=0)

        self.installEventFilter(self)
        # NOTE end diverge

        restoreGeom(self, "editcurrent")
        gui_hooks.state_did_reset.append(self.onReset)
        self.mw.requireReset()
        self.show()
        # reset focus after open, taking care not to retain webview
        # pylint: disable=unnecessary-lambda
        self.mw.progress.timer(100, lambda: self.editor.web.setFocus(), False)

    def reopen(self, mw):
        self.show()

    def setNote(self, note):
        self.editor.setNote(note)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Leave and self.mw.reviewer.state == 'question':
            self.editor.saveNow(self.editor.redrawMainWindow, False)
            self.obscureEditor()
            return False

        else:
            return super().eventFilter(obj, event)

    def obscureEditor(self):
        self.editor.maybeObscureAll()

    def unobscureEditor(self):
        self.editor.unobscureAll()

    def _saveAndClose(self) -> None:
        gui_hooks.state_did_reset.remove(self.onReset)

        # NOTE diverge from Anki
        self.editor.cleanup()

        saveGeom(self, "editcurrent")
        aqt.dialogs.markClosed("EditCurrent")
        QDialog.reject(self)

def init_editcurrent():
    dialogs.register_dialog('EditCurrent', PersistentEditCurrent, None)
