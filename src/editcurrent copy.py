from aqt import mw, QEvent
from aqt.editcurrent import EditCurrent
from aqt.gui_hooks import webview_will_set_content

from anki.hooks import wrap
from anki.lang import _

from .editor_helper import obscure_if_question
from .reviewer_helper import redraw_reviewer
from .utils import base_path


def setup_editcurrent(web_content, context):
    if hasattr(context, 'parentWindow') and isinstance(context.parentWindow, EditCurrent):
        editcurrent = context.parentWindow

        web_content.css.append(f'{base_path}/editcurrent.css')
        web_content.js.append(f'{base_path}/editcurrent.js')

        editcurrent.setWindowTitle(_("Persistent Edit Current"))
        editcurrent.installEventFilter(context.parentWindow)

def persistent_show(self):
    super(EditCurrent, self).show()

    if self.mw.reviewer.state == 'question':
        self.editor.loadNote()
        obscure_if_question(self.editor)

def reshow(self, mw, _old):
    self.show()

def eventFilter(self, obj, event):
    if (
        event.type() == QEvent.Leave and
        self.mw.reviewer.state == 'question' and
        not self.editor.presentation_mode
    ):
        def after():
            redraw_reviewer(self.mw.reviewer)
            if not getattr(self, 'do_not_overwrite', False):
                self.do_not_overwrite = False
                obscure_if_question(self.editor)

        if self.editor.web:
            self.editor.saveNow(after, False)

        return False

    return super(EditCurrent, self).eventFilter(obj, event)

def init_editcurrent():
    webview_will_set_content.append(setup_editcurrent)

    EditCurrent.show = persistent_show
    EditCurrent.reopen = wrap(EditCurrent.reopen, reshow, pos='around')
    EditCurrent.eventFilter = eventFilter
