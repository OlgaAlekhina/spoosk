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


// colorBars

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


function byteToSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    if (!bytes) {
        return '0 Byte'
    }
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)))
    return Math.round(bytes / Math.pow(1024, i)) + ' ' + sizes[i];
}

file_list = [];

// uploading photos to preview in the review form
function upload(selector, options = {}) {

    let files = []
    const input = document.getElementById(selector)
    const maxImages = options.maxImages || 5;
    let currentImages = 0;

    if (options.multi) {
        input.setAttribute('multiple', true)
    }

    if (options.accept && Array.isArray(options.accept)) {
        input.setAttribute('accept', options.accept.join(','))
    }

    const label = document.querySelector('.foto-field');
    const fotoContainer = document.querySelector('.foto-container')

    const changeHandler = event => {
        console.log(event.target.files.length)
        if (!event.target.files.length || currentImages > maxImages) {
            return
        }

        files = Array.from(event.target.files)

        let number = maxImages - currentImages

        for (let i = 0; i < Math.min(files.length, number); i++) {
            const file = files[i];
            // add chosen file to the list
            file_list.push(file);

            if (!file.type.match('image')) {
                continue;
            }

            const reader = new FileReader()

            reader.onload = ev => {
                const src = ev.target.result
                fotoContainer.insertAdjacentHTML('beforeend', `
                    <div class="preview-image">
                        <div class="preview-remove" data-name=${file.name}>&times;</div>
                        <img src="${src}" alt="${file.name}">
                        <div class="preview-info">
                            ${byteToSize(file.size)}
                        </div>
                    </div>
                `)
            }

            reader.readAsDataURL(file)

            currentImages++;
            if (currentImages >= maxImages) {
                input.setAttribute('disabled', true);
                label.style.display = 'none';
            } else {
                input.removeAttribute('disabled');
                label.style.display = 'block';
            }
        }
    }

    const removeHandler = event => {
        console.log('event', event.target.dataset)
        if (!event.target.dataset.name) {
            return
        }

        const {name} = event.target.dataset
        files = files.filter(file => file.name !== name)

        const block = fotoContainer.querySelector(`[data-name="${name}"]`).closest('.preview-image')

        block.classList.add('removing')
        setTimeout(() => block.remove(), 300)

        currentImages--;
        if (currentImages < maxImages) {
            input.removeAttribute('disabled');
            label.style.display = 'block';
        }
    }

    input.addEventListener('change', changeHandler)
    fotoContainer.addEventListener('click', removeHandler)
}

upload('foto_review', {
    multi: true,
    accept: ['.png', '.jpg', '.jpeg'],
    maxImages: 5,
})


