from aqt import mw

flip_keyword = 'persistent_flip_card'
presentation_keyword = 'persistent_presentation_mode'
presentation_shortcut_keyword = 'persistent_presentation_shortcut'

addon_package = mw.addonManager.addonFromModule(__name__)
base_path = f'/_addons/{addon_package}/web'
