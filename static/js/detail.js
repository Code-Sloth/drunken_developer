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

  const starBtns = box.querySelectorAll('.comment_star')
  const starRating = box.querySelector('#star_rating')
  const starContent = box.querySelector('.comment-star-content')

  starBtns.forEach((bt) => {
    const img = bt.querySelector('img')
    const attr = bt.getAttribute('data-value')

    if (attr <= starRating.value) {
      img.src = "/static/image/star1.svg"
      img.alt = "star1"
    } else {
      img.src = "/static/image/graystar1.svg"
      img.alt = "graystar1"
    }
  })

  starBtns.forEach((btn) => {
    btn.addEventListener('click', (event) => {
      const value = event.target.getAttribute('data-value')

      if (value == 1) {
        starContent.textContent = '나쁨'
      } else if (value == 2) {
        starContent.textContent = '별로'
      } else if (value == 3) {
        starContent.textContent = '보통'
      } else if (value == 4) {
        starContent.textContent = '좋음'
      } else if (value == 5) {
        starContent.textContent = '최고'
      }

      starRating.value = value
      starBtns.forEach((bt) => {
        const img = bt.querySelector('img')
        const attr = bt.getAttribute('data-value')

        if (attr <= value) {
          img.src = "/static/image/star1.svg"
          img.alt = "star1"
        } else {
          img.src = "/static/image/graystar1.svg"
          img.alt = "graystar1"
        }
      })
    })
  })

  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  if (commentForm) {

    commentForm.addEventListener('submit', (event) => {
      event.preventDefault()
  
      const productId = event.target.dataset.userId
      const commentId = commentForm.querySelector('.comment_pk').value
      const formData = new FormData(commentForm)
      formData.append('csrfmiddlewaretoken', csrftoken)
      formData.append('star-rating', starRating.value)

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

          const commentStarStar = box.querySelector('.comment-star-star')
          const commentStarCount = box.querySelector('.comment-star-count')
          const commentStar = response.data.commentStar_count

          commentStarStar.style['width'] = `${commentStar*20}%`
          commentStarCount.textContent = commentStar

        })

        .catch((error) => {
          console.log(error.response)
        })
    })
  }
})
