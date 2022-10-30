const title = document.getElementById('title')
const content = document.getElementById('content')
const form = document.getElementById('demo-form2')
const errorMessage =document.getElementById('errorMessage')
const errorDiv =document.getElementById('errorDiv')

form.addEventListener('submit', (e) => {
  let messages = []
  
  if (title.value.length < 8) {
    console.log("passeia")
    messages.push('Título é demasiado curto')
  }

  if (content.value.length < 20) {
    console.log("passeiaki")
    messages.push('A descrição tem que ter no mínimo 20 caracteres')
  }

  if (contact.value.length <  9 && contact.value.length > 0) {
    messages.push('O seu contacto tem que ter no mínimo 9 caracteres')
  }
  if (messages.length > 0) {
    e.preventDefault()
    errorDiv.style.display = 'block'
    errorMessage.innerText = messages.join(';')
  }
})
