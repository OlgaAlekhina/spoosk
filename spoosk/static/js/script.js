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


/*--------------------colorBars----------------------------------*/

colorBars = document.querySelectorAll('.count-trails-list');

colorBars.forEach( function (bar) {
    const b = bar.querySelectorAll('.color-bar')
    let total_count = 0
    const countsTrail = {}
    for (let i = 0; i < b.length; i++) {
        let level = b[i].classList[1]
        let count = b[i].innerHTML
        total_count += Number(count)
        countsTrail[level] = count
    };

    let percentByLevel = {};
    for (const [level, counts] of Object.entries(countsTrail)) {
        percentByLevel[level] = Math.fround(counts / total_count * 100);
    };

    for (let i = 0; i < b.length; i++) {
        let level = b[i].classList[1];
        let percent = percentByLevel[level];
        b[i].style.width = percent + '%';
      }

});
