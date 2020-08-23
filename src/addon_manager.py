from aqt import mw

from ..gui.settings import Settings

from .utils import (
    flip_keyword,
    presentation_keyword,
    presentation_shortcut_keyword,
)

def set_settings(
    flip_shortcut: str,
    presentation_mode: bool,
    presentation_shortcut: str,
):
    mw.pm.profile[flip_keyword] = flip_shortcut
    mw.pm.profile[presentation_keyword] = presentation_mode
    mw.pm.profile[presentation_shortcut_keyword] = presentation_shortcut

def show_settings():
    dialog = Settings(mw, set_settings)

    flip = mw.pm.profile.get(flip_keyword, 'C')
    presentation_mode = mw.pm.profile.get(presentation_keyword, False)
    presentation_shortcut = mw.pm.profile.get(presentation_shortcut_keyword, 'Ctrl+P')

    dialog.setupUi(flip, presentation_mode, presentation_shortcut)
    return dialog.exec_()

def init_addon_manager():
    mw.addonManager.setConfigAction(__name__, show_settings)
