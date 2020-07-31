from aqt import dialogs, gui_hooks, Qt, QDialog, QKeySequence, QDialogButtonBox
from aqt.qt import qconnect
from aqt.editor import Editor
from aqt.editcurrent import EditCurrent

from aqt.utils import restoreGeom, saveGeom, tooltip
from aqt.gui_hooks import editor_did_init, editor_did_init_shortcuts

from .reviewer import toggle_reviewer

class PersistentEditor(Editor):
    def redrawMainWindow(self):
        reviewer = self.mw.reviewer

        # Maybe reviewer already finished
        if reviewer.card is None:
            return

        # Trigger redrawing of mw without losing focus
        reviewer.card.load()
        reviewer.triggerObscure = False

        toggle_reviewer(reviewer)

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
            self.saveNow(callback, keepFocus)

    # override methods

    def mungeHTML(self, txt):
        return super().mungeHTML(txt.replace('<div class="coverup"></div>', ''))

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

def alter_on_html(cuts, editor):
    if isinstance(editor.parentWindow, EditCurrent):
        def onHtmlEdit_persistent():
            field = editor.currentField

            def callback():
                nonlocal field
                editor._onHtmlEdit(field)
                editor.maybeObscureAll()
                editor.redrawMainWindow()

            editor.saveNow(callback)

        try:
            result = next(filter(lambda v: v[0] == 'Ctrl+Shift+X', cuts))
        except StopIteration:
            return

        del cuts[cuts.index(result)]
        cuts.append(('Ctrl+Shift+X', onHtmlEdit_persistent))

        # NOTE the markChanged property will identify this editor as being an editor within an editcurrent
        editor.markChanged = False

def setup_editor(editor):
    if isinstance(editor.parentWindow, EditCurrent):
        qconnect(editor.tags.lostFocus, editor.redrawMainWindow)

def init_editor():
    # is executed before editor_did_init
    editor_did_init_shortcuts.append(alter_on_html)
    editor_did_init.append(setup_editor)
