const sideBar = document.querySelectorAll('.side-bar');
const itemElements = document.querySelectorAll('.item');

for (var i = 0; i < sideBar.length; i++) {
  sideBar[i].addEventListener('click', function () {
    sideBar.forEach(e => {
      e.classList.remove('active');
    })
    this.classList.add('active');
    let sideBarValue = this.getAttribute('data-li');
    console.log(sideBarValue)
    itemElements.forEach(e => {
      e.classList.add('d-none');
    })
    document.querySelector('.' + sideBarValue).classList.remove('d-none');
  })
}