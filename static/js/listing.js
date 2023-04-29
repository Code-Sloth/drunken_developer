// 콜랩스 색깔, 이미지 변환
const filterBtns = document.querySelectorAll('.filtering-btn')

filterBtns.forEach((btn) => {
  const btnName = btn.getAttribute('name')
  const btnTitle = btn.querySelector('.filtering-title > p')
  const Url = window.location.href
  const filters = btn.querySelectorAll('.filtering')

  if (Url.includes(btnName)) {
    btn.style['border'] = '1px solid rgb(81 151 242)'
    btn.value = true
    btnTitle.style['color'] = 'rgb(81 151 242)'
    btnTitle.style['font-weight'] = 'bold'
  } else { btn.value = false }


  filters.forEach((filter) => {
    const filterCheck = filter.querySelector('.filtering-check > img')
    const fName = filter.getAttribute('name')
    const fValue = filter.getAttribute('value')

    if (Url.includes(`${fName}=${fValue}`)) {
      filterCheck.src = '/static/image/check.png'
      filterCheck.alt = 'check'
    }

  })
  
  if (btn.value == false) {
    const filterCollapse = btn.querySelector('.filtering-collapse')
    const filterArrow = btn.querySelector('.filtering-img > img')

    filterCollapse.addEventListener('show.bs.collapse', () => {
      btn.style.border = '1px solid rgb(81 151 242)'
      filterArrow.style.transform = 'rotate(180deg)'
    })
    
    filterCollapse.addEventListener('hide.bs.collapse', () => {
      btn.style.border = '1px solid rgb(240 240 240)'
      filterArrow.style.transform = ''
    })

  }
})

// 배너 스타일 변환
const banner = document.querySelector('.listing-banner')
const bannerTitle = document.querySelector('.listing-banner-title')
const bannerContent = document.querySelector('.listing-banner-content')
const bannerImage = document.querySelector('.listing-banner-image > img')
const Url = window.location.href

if (Url.includes('category=traditional')) {

  banner.style['background-color'] = 'rgb(255, 251, 244)'
  bannerTitle.textContent = '전통주'
  bannerContent.textContent = '맛있는 막걸리는 여기 다 있어요.'
  bannerImage.src = '/static/image/전통주.png'
  bannerImage.alt = '전통주'

} else if (Url.includes('category=beer')) {

  banner.style['background-color'] = 'rgb(242, 236, 255)'
  bannerTitle.textContent = '맥주'
  bannerContent.textContent = '시원한 맥주들이 모여있어요.'
  bannerImage.src = '/static/image/맥주.png'
  bannerImage.alt = '맥주'

} else if (Url.includes('category=whiskey')) {

  banner.style['background-color'] = 'rgb(247, 250, 253)'
    bannerTitle.textContent = '위스키'
    bannerContent.textContent = '하루를 끝내기에 좋은 술이에요.'
    bannerImage.src = '/static/image/위스키.svg'
    bannerImage.alt = '위스키'

} else if  (Url.includes('category=wine')) {

  banner.style['background-color'] = 'rgb(255, 242, 245)'
  bannerTitle.textContent = '와인'
  bannerContent.textContent = '분위기에는 와인이죠.'
  bannerImage.src = '/static/image/와인.svg'
  bannerImage.alt = '와인'

}


// 필터링


// 가격 외
const buttons = document.querySelectorAll('.filtering')

buttons.forEach((btn) => {

  const btnName = btn.getAttribute('name')
  const btnValue = btn.getAttribute('value')

  btn.addEventListener('click', () => {
    const Url = window.location.href

    if (Url.includes(`&${btnName}=${btnValue}`)) {

      const newUrl = Url.replace(`&${btnName}=${btnValue}`,'')
      window.location.href = newUrl

    } else {

      const newUrl = `${Url}&${btnName}=${btnValue}`
      window.location.href = newUrl
      
    }
    
  })
})


// 가격
const prices = document.querySelectorAll('.pricing')

prices.forEach((price) => {

  const priceName = price.getAttribute('name')
  const priceValue = price.getAttribute('value')

  price.addEventListener('click', () => {
    const Url = window.location.href   

    if (Url.includes(`&${priceName}=${priceValue}`)) {

      const newUrl = Url.replace(`&${priceName}=${priceValue}`,'')
      window.location.href = newUrl

    } else {

      // let reUrl = Url.replace('&price=0,10000','')
      // reUrl = reUrl.replace('&price=10000,30000','')
      // reUrl = reUrl.replace('&price=30000,50000','')
      // reUrl = reUrl.replace('&price=50000,100000','')
      // reUrl = reUrl.replace('&price=100000,1000000','')
  
      const reUrl = Url.replace(/&price=\d+,\d+/g,'')

      const newUrl = `${reUrl}&price=${priceValue}`
      window.location.href = newUrl

    }
  })
})

// 가격 검색
const priceSubmit = document.querySelector('.price-search-submit')

priceSubmit.addEventListener('click', (event) => {
  const num1 = document.querySelector('.price-number1').value
  const num2 = document.querySelector('.price-number2').value

  const Url = window.location.href
  const reUrl = Url.replace(/&price=\d+,\d+/g,'')
  const newUrl = `${reUrl}&price=${num1},${num2}`

  window.location.href = newUrl
})

// sort
const sortBtns = document.querySelectorAll('.sort-btn')

sortBtns.forEach((btn) => {
  btn.addEventListener('click', (event) => {
    const btnValue = btn.value

    sortUrl = window.location.href
    const reUrl = sortUrl.replace(/&sort=[\w\d]+/g,'')
    const newUrl = `${reUrl}&sort=${btnValue}`

    window.location.href = newUrl
    
  })
})

const sortTitle = document.querySelector('.sort-title')
const params = new URLSearchParams(window.location.search)
const sortValue = params.get('sort')

if (sortValue == 'recommend') {
  sortTitle.textContent = '추천순'
} else if (sortValue == 'recent') {
  sortTitle.textContent = '최신순'
} else if (sortValue == 'rating') {
  sortTitle.textContent = '평점순'
} else if (sortValue == 'review') {
  sortTitle.textContent = '리뷰많은순'
} else if (sortValue == 'high') {
  sortTitle.textContent = '높은가격순'
} else if (sortValue == 'low') {
  sortTitle.textContent = '낮은가격순'
}
