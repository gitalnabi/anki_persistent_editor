from aqt.reviewer import Reviewer
from aqt import dialogs, gui_hooks

def get_editcurrent():
    return dialogs._dialogs['EditCurrent'][1]

class PersistentReviewer(Reviewer):
    def nextCard(self):
        super().nextCard()

        current_editcurrent = get_editcurrent()
        if current_editcurrent:
            if self.card:
                current_editcurrent.setNote(self.card.note())
                current_editcurrent.obscureEditor()
            else:
                # reviewer finished and has gone to overview
                current_editcurrent.saveAndClose()

    def _showQuestion(self, triggerObscure=True):
        super()._showQuestion()

        current_editcurrent = get_editcurrent()

        # only if card was flipped
        if triggerObscure and current_editcurrent:
            current_editcurrent.obscureEditor()

    def _showAnswer(self, triggerObscure=True):
        super()._showAnswer()

        current_editcurrent = get_editcurrent()

        # only if card was flipped
        if triggerObscure and current_editcurrent:
            current_editcurrent.unobscureEditor()

def close_editcurrent():
    current_editcurrent = get_editcurrent()
    if current_editcurrent:
        current_editcurrent.saveAndClose()

def init_reviewer():
    gui_hooks.reviewer_will_end.append(close_editcurrent)
