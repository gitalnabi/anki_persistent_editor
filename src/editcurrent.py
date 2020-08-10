from aqt import mw, QEvent
from aqt.editcurrent import EditCurrent
from aqt.gui_hooks import webview_will_set_content

from anki.hooks import wrap

from .editor_helper import maybe_obscure_all
from .reviewer_helper import redraw_reviewer

addon_package = mw.addonManager.addonFromModule(__name__)
base_path = f'/_addons/{addon_package}/web'

mw.addonManager.setWebExports(__name__, r'(web|icons)/.*\.(js|css|png)')

def setup_editcurrent(web_content, context):
    if hasattr(context, 'parentWindow') and isinstance(context.parentWindow, EditCurrent):
        editcurrent = context.parentWindow

        web_content.css.append(f'{base_path}/persistent.css')
        web_content.js.append(f'{base_path}/persistent.js')

        editcurrent.setWindowTitle(_("Persistent Edit Current"))
        editcurrent.installEventFilter(context.parentWindow)

def persistent_show(self):
    super(EditCurrent, self).show()

    if self.mw.reviewer.state == 'question':
        self.editor.loadNote()
        maybe_obscure_all(self.editor)

def reshow(self, mw, _old):
    self.show()

def change_mw_state(self):
    self.mw.state = 'persistentReview'

def eventFilter(self, obj, event):
    if event.type() == QEvent.Leave and self.mw.reviewer.state == 'question':
        def after():
            redraw_reviewer(self.mw.reviewer)
            maybe_obscure_all(self.editor)

        if self.editor.web:
            self.editor.saveNow(after, False)
        return False

    return super(EditCurrent, self).eventFilter(obj, event)

def init_editcurrent():
    webview_will_set_content.append(setup_editcurrent)

    EditCurrent.show = persistent_show
    EditCurrent.reopen = wrap(EditCurrent.reopen, reshow, pos='around')
    EditCurrent._saveAndClose = wrap(EditCurrent._saveAndClose, change_mw_state, pos='before')
    EditCurrent.eventFilter = eventFilter
