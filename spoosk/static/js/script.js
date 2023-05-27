const searchBth = document.querySelector('.search-btn')
const cancelBth = document.querySelector('.cancel-btn')
const searchInput = document.querySelector('.search-input')
const searchBox= document.querySelector('.search-box')
const main = document.querySelector('main')

searchBth.addEventListener('click', function (e) {
    e.stopPropagation();
    searchInput.classList.add('active');
    cancelBth.classList.add('active');
    searchBth.classList.add('active');
});


cancelBth.addEventListener('click', function (e) {
    if (e.target !== searchBox) {
        searchInput.classList.remove('active');
        cancelBth.classList.remove('active');
        searchBth.classList.remove('active');
        searchInput.value = "";
    }
});


main.addEventListener('click', function (e) {
    if (e.target !== searchBox) {
        searchInput.classList.remove('active');
        cancelBth.classList.remove('active');
        searchBth.classList.remove('active');
        searchInput.value = "";
    }
});

main.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        searchInput.innerHTML = "";
    }
});

// main.addEventListener('click', function (e) {
//     e.stopPropagation();
//     searchBox.classList.remove('active');
//     searchInput.classList.remove('active');
// });



