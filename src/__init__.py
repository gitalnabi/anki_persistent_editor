import aqt
from aqt import dialogs, mw

from .editcurrent import init_editcurrent
from .main import init_mw
from .flip import init_flip_shortcut

def init():
    init_mw()
    init_editcurrent()
    init_flip_shortcut()
