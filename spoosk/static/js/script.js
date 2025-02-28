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
function colorBars() {
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
};

window.addEventListener("load", colorBars);

var favorites = document.getElementById('editing_profile-container');
var filter = document.querySelector('.page-cards');
var targets = [favorites, filter];

const observer = new MutationObserver(colorBars);

targets.forEach((target) => {
    if (target != null) {
        observer.observe(target, {childList: true, subtree: true});
    };
});

function byteToSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    if (!bytes) {
        return '0 Byte'
    }
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)))
    return Math.round(bytes / Math.pow(1024, i)) + ' ' + sizes[i];
}

// global variable used in AJAX to submit and edit review
let file_list = [];
// global variable used in AJAX to edit review
let file_deleted = [];

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
    const fileContainer = document.querySelector('.file-container')

    const changeHandler = event => {
        console.log(event.target.files.length)
        // get number of current preview images
        let preview_images = document.getElementsByClassName('preview-image').length;
        currentImages = preview_images;
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
                fileContainer.insertAdjacentHTML('beforeend', `
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

        const {name} = event.target.dataset;
        const {id} = event.target.dataset;
        files = files.filter(file => file.name !== name)
        // remove file from files list
        file_list = file_list.filter(file => file.name !== name)
        // add file id in file_deleted list
        if (id != null) {file_deleted.push(id);};

        const block = fileContainer.querySelector(`[data-name="${name}"]`).closest('.preview-image')

        block.classList.add('removing')
        setTimeout(() => block.remove(), 300)

        currentImages--;
        if (currentImages < maxImages) {
            input.removeAttribute('disabled');
            label.style.display = 'block';
        }
    }

    input.addEventListener('change', changeHandler)
    fileContainer.addEventListener('click', removeHandler)
}

upload('foto_review', {
    multi: true,
    accept: ['.png', '.jpg', '.jpeg'],
    maxImages: 5,
})


const radioButtons = document.querySelectorAll('.get_value');
const submitButton = document.getElementById('submit_review');

radioButtons.forEach((button) => {
  button.addEventListener('change', (event) => {
    const rating = event.target.value;
    if (rating > 0) {
      submitButton.style.backgroundColor = "#005FF9"; 
      submitButton.style.color= "#ffffff";
      submitButton.style.cursor = "pointer";
    } else {
      submitButton.style.backgroundColor = '';  // Revert to the default color when no rating is selected
    }
  });
});


