var PersistentEditor = {
  obscureColor: 'lavender',

  getField: (index) => document.body.children[2].querySelectorAll('.field')[index],
  getFields: () => document.body.children[2].querySelectorAll('.field'),

  obscure: () => {
    const fields = PersistentEditor.getFields()

    for (const field of fields) {
      field.style.color = PersistentEditor.obscureColor
      field.style.background = PersistentEditor.obscureColor
    }
  },

  obscureField: (index) => {
    const field = PersistentEditor.getField(index)

    field.style.color = PersistentEditor.obscureColor
    field.style.background = PersistentEditor.obscureColor
  },

  unobscure: () => {
    const fields = PersistentEditor.getFields()

    for (const field of fields) {
      field.style.color = ''
      field.style.background = ''
    }
  },

  unobscureField: (index) => {
    const field = PersistentEditor.getField(index)

    field.style.color = ''
    field.style.background = ''
  }
}
