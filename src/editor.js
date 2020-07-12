const PersistentEditor = {
  blurColor: 'lightslategray',
  getFields: () => document.body.children[2].querySelectorAll('.field'),

  blur: () => {
    const fields = PersistentEditor.getFields()

    for (const field of fields) {
      debugger
      field.style.color = PersistentEditor.blurColor
      field.style.background = PersistentEditor.blurColor
    }
  },

  unblur: () => {
    const fields = PersistentEditor.getFields()

    for (const field of fields) {
      field.style.color = ''
      field.style.background = ''
    }
  }
}
