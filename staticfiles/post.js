var el;                                                    

function countCharacters(e) {                                    
  var textEntered, countRemaining, counter;          
  textEntered = document.getElementById('contentarea').value;  
  counter = (document.getElementById('contentarea').maxLength - (textEntered.length));
  countRemaining = document.getElementById('charactersRemaining');
  countRemaining.textContent = counter;
  console.log(counter); 
  if (counter == 0) {
    document.getElementById('charactersRemaining').style.color = "red";
} 
}
el = document.getElementById('contentarea');                   
el.addEventListener('keyup', countCharacters, false);

const content = document.getElementById('contentarea')
const form = document.getElementById('form')
const errorMessage =document.getElementById('errorMessage')
const errorDiv =document.getElementById('errorDiv')

form.addEventListener('submit', (e) => {
  let messages = []
  
  if (content.value.length < 3) {
    messages.push('O post tem que ter no mínimo 3 caracteres.')
  }
  if (messages.length > 0) {
    e.preventDefault()
    errorDiv.style.display = 'block'
    errorMessage.innerText = messages.join(';')
  }
})

