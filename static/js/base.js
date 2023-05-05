const gptForm = document.querySelector('#gpt-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

gptForm.addEventListener('submit', (event) => {
  event.preventDefault()
  
  const qValue = document.querySelector('.gpt-input').value
  const formData = new FormData(gptForm)
  formData.append('gpt-q', qValue)

  axios({
    method: 'POST',
    url: `/products/new_chat/`,
    headers: {'X-CSRFToken': csrftoken},
    data: formData,
  })
    .then((response) => {
      const gptText = document.querySelector('.gpt-response')
      const gptResponse = response.data.gptresponse

      gptText.innerHTML = gptResponse
    })
})
