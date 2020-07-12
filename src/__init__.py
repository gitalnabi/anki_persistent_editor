from aqt.editcurrent import EditCurrent
from aqt import dialogs

from os.path import  join, dirname
from aqt.utils import showText

def get_editor_js() -> str:
    editor_js_file = join(dirname(__file__), 'editor.js')

    with open(editor_js_file, "r", encoding="utf-8") as editor_js:
        return editor_js.read() 

class PersistentEditCurrent(EditCurrent):
    def __init__(self, mw):
        super().__init__(mw)
        self.setWindowTitle(_('Persistent Edit Current'))

        self.editor.web.eval(get_editor_js())
        # self.editor.web.eval('PersistentEditor.blur()')

        self.mw.maybeReset()


def init():
    dialogs.register_dialog('EditCurrent', PersistentEditCurrent, None)
