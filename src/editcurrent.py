import aqt
from aqt import dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox
from aqt.utils import restoreGeom, saveGeom, tooltip

from os.path import  join, dirname
from aqt.utils import showText

from .editor import PersistentEditor

def get_editor_js() -> str:
    editor_js_file = join(dirname(__file__), 'editor.js')

    with open(editor_js_file, "r", encoding="utf-8") as editor_js:
        return editor_js.read() 

class PersistentEditCurrent(QDialog):
    def __init__(self, mw) -> None:
        QDialog.__init__(self, None, Qt.Window)
        mw.setupDialogGC(self)
        self.mw = mw
        self.form = aqt.forms.editcurrent.Ui_Dialog()
        self.form.setupUi(self)
        self.setWindowTitle(_("Persistent Edit Current"))
        self.setMinimumHeight(400)
        self.setMinimumWidth(250)
        self.form.buttonBox.button(QDialogButtonBox.Close).setShortcut(
            QKeySequence("Ctrl+Return")
        )
        self.editor = PersistentEditor(self.mw, self.form.fieldsArea, self)
        self.editor.card = self.mw.reviewer.card
        self.editor.setNote(self.mw.reviewer.card.note()) #, focusTo=0)
        self.editor.web.eval(get_editor_js())

        restoreGeom(self, "editcurrent")
        gui_hooks.state_did_reset.append(self.onReset)
        # self.mw.requireReset()
        self.show()
        # reset focus after open, taking care not to retain webview
        # pylint: disable=unnecessary-lambda
        self.mw.progress.timer(100, lambda: self.editor.web.setFocus(), False)

    def onReset(self) -> None:
        # lazy approach for now: throw away edits
        try:
            n = self.editor.note
            n.load()  # reload in case the model changed
        except:
            # card's been deleted
            gui_hooks.state_did_reset.remove(self.onReset)
            self.editor.setNote(None)
            self.mw.reset()
            aqt.dialogs.markClosed("EditCurrent")
            self.close()
            return
        self.editor.setNote(n)

    def reopen(self, mw):
        tooltip("Please finish editing the existing card first.")
        self.onReset()

    def reject(self):
        self.saveAndClose()

    def saveAndClose(self):
        self.editor.saveNow(self._saveAndClose)

    def _saveAndClose(self) -> None:
        gui_hooks.state_did_reset.remove(self.onReset)
        r = self.mw.reviewer
        try:
            r.card.load()
        except:
            # card was removed by clayout
            pass
        else:
            self.mw.reviewer.cardQueue.append(self.mw.reviewer.card)
        self.editor.cleanup()
        self.mw.moveToState("review")
        saveGeom(self, "editcurrent")
        aqt.dialogs.markClosed("EditCurrent")
        QDialog.reject(self)

    def closeWithCallback(self, onsuccess):
        def callback():
            self._saveAndClose()
            onsuccess()

        self.editor.saveNow(callback)
