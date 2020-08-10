def toggle_reviewer(reviewer):
    state = reviewer.state

    if state == 'question':
        reviewer._getTypedAnswer()

    elif state == 'answer':
        reviewer._showQuestion()

def refresh_reviewer(reviewer):
    state = reviewer.state

    if state == 'question':
        reviewer._showQuestion()

    elif state == 'answer':
        reviewer._getTypedAnswer()

def redraw_reviewer(reviewer):
    # Maybe reviewer already finished
    if reviewer.card is None:
        return

    # Trigger redrawing of mw without losing focus
    reviewer.card.load()
    reviewer.triggerObscure = False

    refresh_reviewer(reviewer)
