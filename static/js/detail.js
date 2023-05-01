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
