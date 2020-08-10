from aqt import mw, dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox
from aqt.qt import qconnect
from aqt.editor import Editor
from aqt.editcurrent import EditCurrent

from aqt.utils import restoreGeom, saveGeom, tooltip
from aqt.gui_hooks import editor_did_init, editor_did_init_shortcuts

from .reviewer import refresh_reviewer

def redraw_main_window(editor):
    reviewer = editor.mw.reviewer

    # Maybe reviewer already finished
    if reviewer.card is None:
        return

    # Trigger redrawing of mw without losing focus
    reviewer.card.load()
    reviewer.triggerObscure = False

    refresh_reviewer(reviewer)

def maybe_obscure_all(editor):
    if editor.mw.reviewer.state == 'question':
        editor.web.eval('PersistentEditor.obscure()')

def unobscure(editor, field):
    editor.web.eval(f'PersistentEditor.unobscureField({field})')

def unobscure_all(editor):
    editor.web.eval('PersistentEditor.unobscure()')

def alter_on_html(cuts, editor):
    if isinstance(editor.parentWindow, EditCurrent):
        def on_html_edit_persistent():
            field = editor.currentField

            def callback():
                nonlocal field
                editor._onHtmlEdit(field)
                maybe_obscure_all(editor)
                redraw_main_window(editor)

            editor.saveNow(callback)

        try:
            result = next(filter(lambda v: v[0] == 'Ctrl+Shift+X', cuts))
        except StopIteration:
            return

        del cuts[cuts.index(result)]
        cuts.append(('Ctrl+Shift+X', on_html_edit_persistent))

def setup_editor(editor):
    if isinstance(editor.parentWindow, EditCurrent):
        qconnect(editor.tags.lostFocus, lambda: redraw_main_window(editor))

def init_editor():
    # is executed before editor_did_init
    editor_did_init_shortcuts.append(alter_on_html)
    editor_did_init.append(setup_editor)
