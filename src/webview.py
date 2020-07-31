
from aqt.gui_hooks import webview_will_set_content

from aqt import mw
from aqt.editcurrent import EditCurrent
from aqt.editor import Editor

from aqt.utils import showText

addon_package = mw.addonManager.addonFromModule(__name__)
base_path = f'/_addons/{addon_package}/web'

mw.addonManager.setWebExports(__name__, r'(web|icons)/.*\.(js|css|png)')

def setup_editcurrent(web_content, context):
    if isinstance(context, Editor) and isinstance(context.parentWindow, EditCurrent):
        web_content.css.append(f'{base_path}/persistent.css')
        web_content.js.append(f'{base_path}/persistent.js')

        context.parentWindow.setWindowTitle(_("Persistent Edit Current"))
        context.parentWindow.installEventFilter(context.parentWindow)

def init_webview():
    webview_will_set_content.append(setup_editcurrent)
