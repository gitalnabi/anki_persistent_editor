
from aqt import dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox
from aqt.qt import qconnect
from aqt.editor import Editor
from aqt.utils import restoreGeom, saveGeom, tooltip

from os.path import  join, dirname
from aqt.utils import showText

class PersistentEditor(Editor):
    def redrawMainWindow(self):
        # Trigger redrawing of mw without losing focus
        self.mw.reviewer.card.load()

        if self.mw.reviewer.state == 'question':
            self.mw.reviewer._showQuestion()
        else:
            self.mw.reviewer._showAnswer()

    def setupTags(self):
        super().setupTags()
        qconnect(self.tags.lostFocus, self.redrawMainWindow)

    def onBridgeCmd(self, cmd) -> None:
        if not self.note:
            # shutdown
            return
        # focus lost or key/button pressed?
        if cmd.startswith("blur") or cmd.startswith("key"):
            (type, ord, nid, txt) = cmd.split(":", 3)
            ord = int(ord)
            try:
                nid = int(nid)
            except ValueError:
                nid = 0
            if nid != self.note.id:
                print("ignored late blur")
                return
            txt = self.mungeHTML(txt)
            # misbehaving apps may include a null byte in the text
            txt = txt.replace("\x00", "")
            # reverse the url quoting we added to get images to display
            txt = self.mw.col.media.escapeImages(txt, unescape=True)
            self.note.fields[ord] = txt
            if not self.addMode:
                self.note.flush()
                # self.mw.requireReset()
            if type == "blur":
                self.currentField = None
                # run any filters
                if gui_hooks.editor_did_unfocus_field(False, self.note, ord):
                    # something updated the note; update it after a subsequent focus
                    # event has had time to fire
                    self.mw.progress.timer(100, self.loadNoteKeepingFocus, False)
                else:
                    self.checkValid()
            else:
                gui_hooks.editor_did_fire_typing_timer(self.note)
                self.mw.progress.timer(100, self.redrawMainWindow, False)
                self.checkValid()
        # focused into field?
        elif cmd.startswith("focus"):
            (type, num) = cmd.split(":", 1)
            self.currentField = int(num)
            gui_hooks.editor_did_focus_field(self.note, self.currentField)
        elif cmd in self._links:
            self._links[cmd](self)
        else:
            print("uncaught cmd", cmd)

# gui_hooks.editor_did_init(self)
# gui_hooks.editor_did_focus_field(self.note, self.currentField)
# gui_hooks.editor_did_unfocus_field(False, self.note, ord):
# gui_hooks.editor_did_fire_typing_timer(self.note)
