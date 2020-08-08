from aqt import mw
from aqt.editor import Editor
from aqt.editcurrent import EditCurrent

from aqt.gui_hooks import (
    webview_did_receive_js_message,
)

def persistent_functions(handled, message, context: Editor):
    if isinstance(context, Editor) and isinstance(context.parentWindow, EditCurrent):
        if message.startswith('key'):
            pass
        elif message.startswith('focus'):
            pass
        elif message.startswith('blur'):
            pass

    return handled

def init_webview():
    webview_did_receive_js_message.append(persistent_functions)
