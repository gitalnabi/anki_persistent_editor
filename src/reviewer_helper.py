from anki.rsbackend import NotFoundError


def currently_shows_question(reviewer):
    state = reviewer.state

    if state == "question":
        return True
    elif state == "answer":
        return False

    raise Exception("Should never happen: Reviewer has invalid state")


def toggle_reviewer(reviewer):
    if currently_shows_question(reviewer):
        reviewer._getTypedAnswer()
    else:
        reviewer._showQuestion()


def refresh_reviewer(reviewer):
    if currently_shows_question(reviewer):
        reviewer._showQuestion()
    else:
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
