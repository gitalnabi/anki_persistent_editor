from aqt import dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox
from aqt.qt import qconnect
from aqt.editor import Editor
from aqt.editcurrent import EditCurrent

from aqt.utils import restoreGeom, saveGeom, tooltip
from aqt.gui_hooks import editor_did_init

class PersistentEditor(Editor):
    def redrawMainWindow(self):
        reviewer = self.mw.reviewer

        # Maybe reviewer already finished
        if reviewer.card is None:
            return

        # Trigger redrawing of mw without losing focus
        reviewer.card.load()
        reviewer.triggerObscure = False

        reviewer._showQuestion() if reviewer.state == 'question' else reviewer._showAnswer()

    def maybeObscureAll(self):
        if self.mw.reviewer.state == 'question':
            self.web.eval('PersistentEditor.obscure()')

    def unobscure(self):
        self.web.eval(f'PersistentEditor.unobscureField({self.currentField})')

    def unobscureAll(self):
        self.web.eval('PersistentEditor.unobscure()')

    def saveNowIfNecessary(self, callback, keepFocus=False):
        # avoid constant blinking on hover
        if hasattr(self, 'markChanged') and self.markChanged:
            from aqt.utils import showText
            showText('meh')
            self.saveNow(callback, keepFocus)

    # override methods

    def mungeHTML(self, txt):
        return super().mungeHTML(txt.replace('<div class="coverup"></div>', ''))

    def onHtmlEdit(self):
        field = self.currentField

        def callback():
            nonlocal field
            self._onHtmlEdit(field)
            self.maybeObscureAll()

        self.saveNow(callback)

    def saveNow(self, callback, keepFocus=False):
        super().saveNow(callback, keepFocus)
        self.markChanged = False

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
                self.mw.requireReset()
            if type == "blur":
                self.currentField = None

                # NOTE diverge from Anki
                self.maybeObscureAll()

                # run any filters
                if gui_hooks.editor_did_unfocus_field(False, self.note, ord):
                    # something updated the note; update it after a subsequent focus
                    # event has had time to fire
                    self.mw.progress.timer(100, self.loadNoteKeepingFocus, False)
                else:
                    self.checkValid()
            else:
                gui_hooks.editor_did_fire_typing_timer(self.note)

                # NOTE diverge from Anki
                self.markChanged = True
                self.mw.progress.timer(10, self.redrawMainWindow, False)

                self.checkValid()
        # focused into field?
        elif cmd.startswith("focus"):
            (type, num) = cmd.split(":", 1)
            self.currentField = int(num)

            # NOTE diverge from Anki
            self.unobscure()

            gui_hooks.editor_did_focus_field(self.note, self.currentField)
        elif cmd in self._links:
            self._links[cmd](self)
        else:
            print("uncaught cmd", cmd)

def setup_editor(editor):
    if isinstance(editor.parentWindow, EditCurrent):
        qconnect(editor.tags.lostFocus, editor.redrawMainWindow)

        # NOTE the markChanged property will identify this editor as being an editor within an editcurrent
        editor.markChanged = False

def init_editor():
    editor_did_init.append(setup_editor)
