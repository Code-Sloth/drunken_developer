const commentButtons = document.querySelectorAll('.comment-collapse > div > button')

commentButtons.forEach((btn) => {
  btn.addEventListener('click', (event)=> {
    const btnValue = btn.value

    sortUrl = window.location.href
    const reUrl = sortUrl.replace(/\?.*$/, '')
    const newUrl = `${reUrl}?sort=${btnValue}`

    window.location.href = newUrl
  })
})

const commentSortTitle = document.querySelector('.comment-sort-title')
const params = new URLSearchParams(window.location.search)
const sortValue = params.get('sort')

if (sortValue == 'recent') {
  commentSortTitle.textContent = '최신순'
} else if (sortValue == 'high') {
  commentSortTitle.textContent = '평점높은순'
} else if (sortValue == 'low') {
  commentSortTitle.textContent = '평점낮은순'
}


// 가격 버튼, kakao
const minusBtn = document.querySelector('.minus')
const plusBtn = document.querySelector('.plus')
const number = document.querySelector('.sidebar-number')
const originalPrice = document.querySelector('.original-price')
const price = document.querySelector('.sidebar-price')
const kakaoBtn = document.querySelector('.sidebar-buy')
const kakaoCount = document.querySelector('.kakao-count')

minusBtn.addEventListener('click', (event) => {
  const intNumber = parseInt(number.textContent)
  if (intNumber > 1) {
    number.textContent = intNumber - 1
    originalIntPrice = parseInt(originalPrice.value) * (intNumber-1)

    const afterPrice = originalIntPrice.toLocaleString()

    price.textContent = `${afterPrice}원`

    kakaoBtn.value = originalIntPrice
    kakaoCount.value = intNumber - 1
  }
})

plusBtn.addEventListener('click', (event) => {
  const intNumber = parseInt(number.textContent)
  if (intNumber < 20) {
    number.textContent = intNumber + 1
    originalIntPrice = parseInt(originalPrice.value) * (intNumber+1)

    const afterPrice = originalIntPrice.toLocaleString()

    price.textContent = `${afterPrice}원`

    kakaoBtn.value = originalIntPrice
    kakaoCount.value = intNumber + 1
  }
})

// 댓글 수정

const allBox = document.querySelectorAll('.detail-comment-allbox')

allBox.forEach((box) => {
  const updateBtn = box.querySelector('.update-btn')
  const commentBox = box.querySelector('.comment-contentbox')
  const commentForm = box.querySelector('.comment_form')

  if (updateBtn) {

    updateBtn.addEventListener('click', (event) => {
  
      if (commentBox.classList.contains('d-block')) {
        commentBox.classList.remove('d-block')
        commentBox.classList.add('d-none')
        commentForm.classList.remove('d-none')
        commentForm.classList.add('d-block')
      } else {
        commentBox.classList.remove('d-none')
        commentBox.classList.add('d-block')
        commentForm.classList.remove('d-block')
        commentForm.classList.add('d-none')
      }
    })
  }

  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  if (commentForm) {

    commentForm.addEventListener('submit', (event) => {
      event.preventDefault()
  
      const productId = event.target.dataset.userId
      const commentId = commentForm.querySelector('.comment_pk').value
      const formData = new FormData(commentForm)
      formData.append('csrfmiddlewaretoken', csrftoken)

      axios({
        method: 'POST',
        url: `/products/${productId}/comments/${commentId}/update/`,
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        data: formData,
      })
        .then((response) => {

          if (commentBox.classList.contains('d-block')) {
            commentBox.classList.remove('d-block')
            commentBox.classList.add('d-none')
            commentForm.classList.remove('d-none')
            commentForm.classList.add('d-block')
          } else {
            commentBox.classList.remove('d-none')
            commentBox.classList.add('d-block')
            commentForm.classList.remove('d-block')
            commentForm.classList.add('d-none')
          }

          const commentContent = box.querySelector('.comment-content > p')
          const commentImg = box.querySelector('.comment-img > img')
          const responseContent = response.data.commentContent
          const responseImageUrl = response.data.commentImageUrl

          commentContent.textContent = responseContent
          commentImg.src = responseImageUrl
          commentImg.alt = responseContent

        })

        .catch((error) => {
          console.log(error.response)
        })
    })
  }
})
