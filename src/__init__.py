import aqt
from aqt import dialogs, mw

from .main import init_mw
from .flip import init_flip_shortcut

from .editcurrent import init_editcurrent
from .editor import init_editor
from .reviewer import init_reviewer

def init():
    init_mw()
    init_flip_shortcut()

    init_editcurrent()
    init_editor()
    init_reviewer()
