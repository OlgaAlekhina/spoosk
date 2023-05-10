const searchBth = document.querySelector('.search-btn')
const cancelBth = document.querySelector('.cancel-btn')
const searchInput = document.querySelector('.search-input')
const searchBox= document.querySelector('.search-box')
const main = document.querySelector('main')

searchBth.addEventListener('click', function (e) {
    e.stopPropagation();
    searchBox.classList.add('active');
    searchInput.classList.add('active');
    cancelBth.classList.add('active');
});


document.addEventListener('click', function (e) {
    if (e.target !== searchBox) {
        searchBox.classList.remove('active');
        searchInput.classList.remove('active');
        cancelBth.classList.remove('active');
    }
});

// main.addEventListener('click', function (e) {
//     e.stopPropagation();
//     searchBox.classList.remove('active');
//     searchInput.classList.remove('active');
// });



