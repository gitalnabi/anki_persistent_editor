var PersistentEditor = {
  getField: (index) => document.body.children[2].querySelectorAll('.field')[index],
  getFields: () => document.body.children[2].querySelectorAll('.field'),

  getObscureDiv: () => {
    const obscureDiv = document.createElement('div')
    obscureDiv.classList.add('coverup')

    obscureDiv.addEventListener('click', (event) => {
      event.target.parentElement.removeChild(event.target)
    })

    return obscureDiv
  },

  appendObscureDiv: (field, obscureDiv) => {
    if (!field.querySelector('.coverup')) {
      field.appendChild(obscureDiv)
    }
  },

  obscure: () => {
    if (PersistentEditor.shouldBeFocused !== null) {
      // a blur caused by context menu
      const index = PersistentEditor.shouldBeFocused

      PersistentEditor.shouldBeFocused = null
      PersistentEditor.unobscureField(index)
      // another obscure is triggered from within unobscureField
    }

    else {
      // all other blurs
      const fields = PersistentEditor.getFields()

      for (const field of fields) {
        PersistentEditor.appendObscureDiv(field, PersistentEditor.getObscureDiv())
      }
    }
  },

  obscureField: (index) => {
    const field = PersistentEditor.getField(index)
    PersistentEditor.appendObscureDiv(field, PersistentEditor.getObscureDiv())
  },

  filterObscureDivs: (element) => {
      const obscureDivs = element.querySelectorAll('.coverup')
      for (const od of obscureDivs) {
        od.parentNode.removeChild(od)
      }
  },

  unobscure: () => {
    const fields = PersistentEditor.getFields()

    for (const field of fields) {
      PersistentEditor.filterObscureDivs(field)
    }
  },

  unobscureField: (index) => {
    PersistentEditor.obscure()

    const field = PersistentEditor.getField(index)
    PersistentEditor.filterObscureDivs(field)
  },

  saveSelectionField: () => {
    const selection = window.getSelection()

    const anchor = selection.anchorNode
    const fields = Array.from(document.querySelectorAll('.field'))

    for (const field of fields) {
      if (field.contains(anchor)) {
        const num = field.id.slice(1)
        PersistentEditor.shouldBeFocused = num
      }
    }
  },

  shouldBeFocused: null,
}
