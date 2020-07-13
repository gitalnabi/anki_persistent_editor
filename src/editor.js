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

  obscure: () => {
    const fields = PersistentEditor.getFields()

    for (const field of fields) {
      field.appendChild(PersistentEditor.getObscureDiv())
    }
  },

  obscureField: (index) => {
    const field = PersistentEditor.getField(index)
    field.appendChild(PersistentEditor.getObscureDiv())
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
    const field = PersistentEditor.getField(index)
    PersistentEditor.filterObscureDivs(field)
  },

  appendStyleTag: (input) => {
    var styleSheet = document.createElement('style')
    styleSheet.type = 'text/css'
    styleSheet.innerHTML = input
    globalThis.document.head.appendChild(styleSheet)
  },
}
