from aqt.reviewer import Reviewer
from aqt.utils import showText
from aqt import dialogs

def get_editcurrent():
    return dialogs._dialogs['EditCurrent'][1]

class PersistentReviewer(Reviewer):
    def nextCard(self):
        super().nextCard()

        current_editcurrent = get_editcurrent()
        if current_editcurrent:
            current_editcurrent.setNote(self.card.note())

    def _showQuestion(self):
        super()._showQuestion()

        current_editcurrent = get_editcurrent()
        if current_editcurrent:
            current_editcurrent.obscureEditor()

    def _showAnswer(self):
        super()._showAnswer()

        current_editcurrent = get_editcurrent()
        if current_editcurrent:
            current_editcurrent.unobscureEditor()
