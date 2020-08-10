from anki.rsbackend import NotFoundError

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

    try:
        reviewer.card.load()
        # Skip obscuring of EditCurrent
        reviewer.do_not_reload_editor_if_question = True

        refresh_reviewer(reviewer)

    except NotFoundError:
        # card was deleted (probably in browser)
        # maybe something nicer can be done here:
        # - completely hide fields ?
        # - automatically close editcurrent ?
        pass
