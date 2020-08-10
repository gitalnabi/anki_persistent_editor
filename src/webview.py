from aqt import mw
from aqt.editor import Editor
from aqt.editcurrent import EditCurrent

from aqt.gui_hooks import (
    webview_did_receive_js_message,
)

from .editor import unobscure, maybe_obscure_all
from .reviewer import redraw_reviewer

def persistent_functions(handled, message, context: Editor):
    if isinstance(context, Editor) and isinstance(context.parentWindow, EditCurrent):
        cmd = message.split(':', 1)

        if cmd[0] == 'focus':
            focused_field = cmd[1]
            unobscure(context, focused_field)

        elif cmd[0] == 'key':
            context.mw.progress.timer(10, lambda: redraw_reviewer(context.mw.reviewer), False)

        elif cmd[0] == 'blur':
            maybe_obscure_all(context)

    return handled

def init_webview():
    webview_did_receive_js_message.append(persistent_functions)
