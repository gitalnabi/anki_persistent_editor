import aqt
from aqt import mw, dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox, QEvent
from aqt.qt import qconnect
from aqt.utils import restoreGeom, saveGeom
from aqt.editcurrent import EditCurrent
from aqt.editor import Editor

from aqt.gui_hooks import webview_will_set_content

addon_package = mw.addonManager.addonFromModule(__name__)
base_path = f'/_addons/{addon_package}/web'

mw.addonManager.setWebExports(__name__, r'(web|icons)/.*\.(js|css|png)')

from .editor import maybe_obscure_all, unobscure_all
from .reviewer import redraw_reviewer

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
        self.editor = Editor(self.mw, self.form.fieldsArea, self)
        self.editor.card = self.mw.reviewer.card

        # NOTE diverge from Anki
        if self.mw.reviewer.state == 'question':
            self.editor.setNote(self.mw.reviewer.card.note())
            self.obscureEditor()
        else:
            self.editor.setNote(self.mw.reviewer.card.note(), focusTo=0)
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
            def after():
                redraw_reviewer(self.mw.reviewer)
                self.obscureEditor()

            self.editor.saveNow(after, False)
            return False

        return super().eventFilter(obj, event)

    def obscureEditor(self):
        maybe_obscure_all(self.editor)

    def unobscureEditor(self):
        unobscure_all(self.editor)

    def _saveAndClose(self) -> None:
        gui_hooks.state_did_reset.remove(self.onReset)

        # NOTE diverge from Anki
        self.editor.cleanup()

        saveGeom(self, "editcurrent")
        aqt.dialogs.markClosed("EditCurrent")
        QDialog.reject(self)

def setup_editcurrent(web_content, context):
    if hasattr(context, 'parentWindow') and isinstance(context.parentWindow, EditCurrent):
        editcurrent = context.parentWindow

        web_content.css.append(f'{base_path}/persistent.css')
        web_content.js.append(f'{base_path}/persistent.js')

        editcurrent.setWindowTitle(_("Persistent Edit Current"))
        editcurrent.installEventFilter(context.parentWindow)

def init_editcurrent():
    dialogs.register_dialog('EditCurrent', PersistentEditCurrent, None)
    webview_will_set_content.append(setup_editcurrent)
