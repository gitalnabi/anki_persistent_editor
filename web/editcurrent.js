var removeObscured = (event) => {
  event.currentTarget.editable.classList.remove("is-obscured")
  event.currentTarget.editable.focus()
}

var PersistentEditor = {
  obscureEditable: (field) => {
    if (!field.editingArea.editable.classList.contains("is-obscured")) {
      field.editingArea.editable.classList.add("is-obscured")
      field.editingArea.addEventListener("click", removeObscured, { once: true })
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
      forEditorField([], (field) => {
        PersistentEditor.obscureEditable(field)
      })
    }
  },

  obscureField: (index) => {
    const field = getEditorField(index)
    PersistentEditor.obscureEditable(field)
  },

  unobscureEditable: (field) => {
    field.editingArea.editable.classList.remove("is-obscured")
    field.editingArea.removeEventListener("click", removeObscured)
  },

  unobscure: () => {
    forEditorField([], (field) => {
      PersistentEditor.unobscureEditable(field)
    })
  },

  unobscureField: (index) => {
    PersistentEditor.obscure()
    const field = getEditorField(index)
    PersistentEditor.unobscureEditable(field)
  },

  saveSelectionField: () => {
    const selection = window.getSelection()

    const anchor = selection.anchorNode
    forEditorField([], (field) => {
      if (field.contains(anchor)) {
        const num = field.id.slice(1)
        PersistentEditor.shouldBeFocused = num
      }
    })
  },

  load: () => {
    forEditorField([], (field) => {
      if (!field.hasAttribute("has-persistent")) {
        const style = document.createElement('style');
        style.textContent = `
anki-editable.is-obscured {
  visibility: hidden;
}`

        field.editingArea.shadowRoot.insertBefore(style, field.editingArea.editable)
        field.setAttribute("has-persistent", "")
      }
    })
  },

  shouldBeFocused: null,
}
