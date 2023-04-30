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