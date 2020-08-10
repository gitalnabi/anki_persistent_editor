from aqt import mw

from ..gui.custom.settings import Settings
from .utils import flip_keyword

def set_settings(flip_shortcut):
    mw.pm.profile[flip_keyword] = flip_shortcut

def show_settings():
    dialog = Settings(mw, set_settings)

    flip = mw.pm.profile.get(flip_keyword, 'C')

    dialog.setupUi(flip)
    return dialog.exec_()

def init_addon_manager():
    mw.addonManager.setConfigAction(__name__, show_settings)
