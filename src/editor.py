from aqt import mw, dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox
from aqt.qt import qconnect
from aqt.editor import Editor
from aqt.editcurrent import EditCurrent

from aqt.utils import restoreGeom, saveGeom, tooltip
from aqt.gui_hooks import editor_did_init, editor_did_init_shortcuts

from .reviewer import refresh_reviewer

class PersistentEditor(Editor):
    def redrawMainWindow(self):
        reviewer = self.mw.reviewer

        # Maybe reviewer already finished
        if reviewer.card is None:
            return

        # Trigger redrawing of mw without losing focus
        reviewer.card.load()
        reviewer.triggerObscure = False

        refresh_reviewer(reviewer)

    def maybeObscureAll(self):
        if self.mw.reviewer.state == 'question':
            self.web.eval('PersistentEditor.obscure()')

    def unobscure(self, field):
        self.web.eval(f'PersistentEditor.unobscureField({field})')

    def unobscureAll(self):
        self.web.eval('PersistentEditor.unobscure()')

def alter_on_html(cuts, editor):
    if isinstance(editor.parentWindow, EditCurrent):
        def on_html_edit_persistent():
            field = editor.currentField

            def callback():
                nonlocal field
                editor._onHtmlEdit(field)
                editor.maybeObscureAll()
                editor.redrawMainWindow()

            editor.saveNow(callback)

        try:
            result = next(filter(lambda v: v[0] == 'Ctrl+Shift+X', cuts))
        except StopIteration:
            return

        del cuts[cuts.index(result)]
        cuts.append(('Ctrl+Shift+X', on_html_edit_persistent))

def setup_editor(editor):
    if isinstance(editor.parentWindow, EditCurrent):
        qconnect(editor.tags.lostFocus, editor.redrawMainWindow)

def init_editor():
    # is executed before editor_did_init
    editor_did_init_shortcuts.append(alter_on_html)
    editor_did_init.append(setup_editor)
