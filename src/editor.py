from aqt import mw
from aqt.qt import qconnect
from aqt.editcurrent import EditCurrent
from aqt.gui_hooks import (
    editor_did_init,
    editor_did_init_shortcuts,
    editor_will_show_context_menu,
)
from aqt.utils import tooltip

from .editor_helper import obscure_if_question
from .reviewer_helper import currently_shows_question, redraw_reviewer
from .utils import presentation_mode_keyword, presentation_shortcut_keyword


def toggle_presentation_mode(editor):
    editor.presentation_mode = not editor.presentation_mode

    mode_string = 'presentation' if editor.presentation_mode else 'obscure'
    tooltip(f'Editor changed to {mode_string} mode', parent=editor.parentWindow)

def alter_on_html(cuts, editor):
    if isinstance(editor.parentWindow, EditCurrent):
        def on_html_edit_persistent():
            field = editor.currentField

            def callback():
                nonlocal field
                editor._onHtmlEdit(field)
                obscure_if_question(editor)
                redraw_reviewer(editor.mw.reviewer)

            editor.saveNow(callback)

        try:
            result = next(filter(lambda v: v[0] == 'Ctrl+Shift+X', cuts))
            del cuts[cuts.index(result)]
        except StopIteration:
            return

        cuts.append(('Ctrl+Shift+X', on_html_edit_persistent))

        editor.presentation_mode = mw.pm.profile.get(presentation_mode_keyword, False)
        cuts.append((mw.pm.profile.get(presentation_shortcut_keyword, 'Ctrl+P'), lambda: toggle_presentation_mode(editor)))

def setup_editor(editor):
    if isinstance(editor.parentWindow, EditCurrent):
        qconnect(editor.tags.lostFocus, lambda: redraw_reviewer(editor.mw.reviewer))

def keep_focus_during_context_menu(webview, menu):
    if isinstance(webview.editor.parentWindow, EditCurrent) and currently_shows_question(webview.editor.mw.reviewer):
        # prevents eventFilter to overwrite selection field
        webview.editor.parentWindow.do_not_overwrite = True
        webview.eval('PersistentEditor.saveSelectionField()')

def init_editor():
    # is executed before editor_did_init
    editor_did_init_shortcuts.append(alter_on_html)
    editor_did_init.append(setup_editor)
    editor_will_show_context_menu.append(keep_focus_during_context_menu)
