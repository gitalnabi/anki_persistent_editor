from aqt.editcurrent import EditCurrent

def obscure_if_question(editor):
    if editor.mw.reviewer.state == 'question':
        editor.web.eval('PersistentEditor.obscure()')

def unobscure(editor, field):
    editor.web.eval(f'PersistentEditor.unobscureField({field})')

def unobscure_all(editor):
    editor.web.eval('PersistentEditor.unobscure()')
