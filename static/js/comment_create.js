document.addEventListener('DOMContentLoaded', () => {
  const starBtns = document.querySelectorAll('.comment_star')
  const starRating = document.querySelector('#star_rating')
  const starContent = document.querySelector('.comment-star-content')

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
        console.log(attr)
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
})