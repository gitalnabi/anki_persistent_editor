from aqt import mw
from aqt.editcurrent import EditCurrent


def obscure_if_question(editor):
    if editor.mw.reviewer.state == 'question' and not editor.presentation_mode:
        editor.web.eval('PersistentEditor.obscure()')

def unobscure_if_question(editor, field):
    if editor.mw.reviewer.state == 'question' and not editor.presentation_mode:
        editor.web.eval(f'PersistentEditor.unobscureField({field})')

def unobscure_all(editor):
    if not editor.presentation_mode:
        editor.web.eval('PersistentEditor.unobscure()')
