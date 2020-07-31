from aqt import dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox
from aqt.qt import qconnect
from aqt.editor import Editor
from aqt.utils import restoreGeom, saveGeom, tooltip

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

    def setupTags(self):
        super().setupTags()
        qconnect(self.tags.lostFocus, self.redrawMainWindow)

        # TODO this does not really belong here, but for now it's fine
        self.markChanged = False

    def maybeObscureAll(self):
        if self.mw.reviewer.state == 'question':
            self.web.eval('PersistentEditor.obscure()')

    def unobscure(self):
        self.web.eval(f'PersistentEditor.unobscureField({self.currentField})')

    def unobscureAll(self):
        self.web.eval('PersistentEditor.unobscure()')

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

    def saveNowIfNecessary(self, callback, keepFocus=False):
        # avoid constant blinking on hover
        if self.markChanged:
            self.saveNow(callback, keepFocus)

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
