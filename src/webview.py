from aqt import mw
from aqt.editor import Editor
from aqt.editcurrent import EditCurrent

from aqt.gui_hooks import (
    webview_did_receive_js_message,
)

def persistent_functions(handled, message, context: Editor):
    if isinstance(context, Editor) and isinstance(context.parentWindow, EditCurrent):
        cmd = message.split(':', 1)

        if cmd[0] == 'focus':
            focused_field = cmd[1]
            context.unobscure(focused_field)

        elif cmd[0] == 'key':
            context.mw.progress.timer(10, context.redrawMainWindow, False)

        elif cmd[0] == 'blur':
            context.maybeObscureAll()

    return handled

def init_webview():
    webview_did_receive_js_message.append(persistent_functions)
