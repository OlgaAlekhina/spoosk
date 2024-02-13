const modals = Array.from(document.querySelectorAll('.modal'));
console.log(modals)
const closeModalBtns = Array.from(document.querySelectorAll('.modal__close-btn'));

function resetForms() {
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const resetRequestForm = document.getElementById("reset-request");
    const resetForm = document.getElementById("reset-form");
    const signupResponse = document.getElementById('signup-response');
    const results = document.getElementById('results');
    const resetResults = document.getElementById('reset_results');
    const addingReview = document.getElementById('adding_review');
    const preview = document.querySelector('.preview');

    if (loginForm) loginForm.reset();
    if (signupForm) signupForm.reset();
    if (resetRequestForm) resetRequestForm.reset();
    if (resetForm) resetForm.reset();
    if (signupResponse) signupResponse.innerHTML = "";
    if (results) results.innerHTML = "";
    if (resetResults) resetResults.innerHTML = "";
    if (addingReview) addingReview.reset();
    if (preview) preview.innerHTML = "";
}

function toggleScrollLock() {
  document.body.classList.toggle("no-scroll");
}

function openModal(modal) {
    scrollY = window.scrollY;
    document.body.style.position = 'fixed';
    document.body.style.top = `-${scrollY}px`;

    modal.classList.add("open");
    toggleScrollLock();
}

function closeModal(modal) {
    console.log(modal)
    scrollY = window.scrollY;
    document.body.style.position = 'static';
    window.scrollTo(0, scrollY);

    modal.classList.remove("open");
    toggleScrollLock();
    resetForms();
}

closeModalBtns.forEach((btn, i) => {
    console.log(btn)
    console.log(i)
    btn.addEventListener("click", function () {
        console.log(modals[i])
        closeModal(modals[i]);
    });
});

modals.forEach((modal) => {
    modal.addEventListener("click", function (event) {
        if (!event._isClickWithInModal) {
            closeModal(modal);
        }
    });
});

// Привязка обработчика события "click" для кнопки "Профиль", открытия модального окна авторизации/регистрации
document.getElementById("open-modal-profile-btn").addEventListener("click", function() {
    openModal(document.getElementById("modal-signup-signin"))
});

if (document.getElementById("open-modal-advanced-filters-btn")) {
    document.getElementById("open-modal-advanced-filters-btn").addEventListener("click", function() {
        openModal(document.getElementById("modal-advanced-filters"))
    });
}

// Привязка обработчика события "click" для кнопки "Оставить отзыв на странице курорта"
if (document.getElementById("open-modal-add-review")) {
    document.getElementById("open-modal-add-review").addEventListener("click", function() {
        openModal(document.getElementById("modal-add-review"))
    });
}

// Открыть модальное окно удаления аккаунта
if (document.getElementById("btn-delete-account")) {
    document.getElementById("btn-delete-account").addEventListener("click", function() {
        openModal(document.getElementById("modal-account-delete"))
    });
}

if (document.querySelector(".modal .modal-review__box")) {
    document.querySelector(".modal-review__box").addEventListener('click', function (event) {
      event._isClickWithInModal = true;
    });
}

if (document.querySelector(".modal .modal_box")) {
  document.querySelector(".modal_box").addEventListener('click', function (event) {
    event._isClickWithInModal = true;
  });
}

if (document.querySelector(".modal .form-register__box")) {
  document.querySelector(".modal .form-register__box").addEventListener('click', function (event) {
    event._isClickWithInModal = true;
  });
}

if (document.querySelector(".modal .form-register__box-rec")) {
  document.querySelector(".modal .form-register__box-rec").addEventListener('click', function (event) {
    event._isClickWithInModal = true;
  });
}

if (document.querySelector(".modal .modal-add-review__box")) {
  document.querySelector(".modal .modal-add-review__box").addEventListener('click', function (event) {
    event._isClickWithInModal = true;
  });
}

// Обработчик события "keydown" для закрытия модального окна при нажатии на клавишу Esc
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        const openModalIndex = modals.findIndex(modal => modal.classList.contains("open"));
        if (openModalIndex !== -1) {
            closeModal(modals[openModalIndex]);
        }
    }
});

function clearModalContent() {
    const nameElement = document.querySelector('.review-resort-name');
    const regionElement = document.querySelector('.review-resort-region');
    const textElement = document.querySelector('.review-text');
    const authorElement = document.querySelector('.review-author');
    const starsList = document.querySelector('.stars-list-modal');
    const caruselModal = document.querySelector('.carusel-modal');

    if (nameElement) nameElement.textContent = '';
    if (regionElement) regionElement.textContent = '';
    if (textElement) textElement.textContent = '';
    if (authorElement) authorElement.textContent = '';
    if (starsList) starsList.innerHTML = ''; 
    if (caruselModal) caruselModal.innerHTML = '';

    
 }

function getReviewModalContent(response) {

    const modal = document.getElementById('modal-review-full');

    const nameElement = modal.querySelector('.review-resort-name');
    nameElement.textContent = response.resort_name;

    const urlElement = modal.querySelector('#resort_link');
    urlElement.href = response.resort_url;

    const regionElement = modal.querySelector('.review-resort-region');
    regionElement.textContent = response.resort_region;
  
    const data_at = modal.querySelector('.review-author-date');
    data_at.textContent = response.review_data_at;

    const textElement = modal.querySelector('.review-text').querySelector('p');
    textElement.textContent = response.review_text;

    const authorElement = modal.querySelector('.review-author');
    authorElement.textContent = response.author_name;

    const authorFoto = modal.querySelector('.foto-container-review');
    const avatar = document.createElement('img');
    avatar.classList.add('info-user__foto')
    avatar.src = String(response.author_avatar);
    avatar.alt = 'Аватар';
    authorFoto.appendChild(avatar);

    const rating = response.review_rating;
    const starsList = document.querySelector('.stars-list-modal');
    
    for (let i = 1; i <= 5; i++) {
        let starsItem = document.createElement('li');
        starsItem.classList.add("stars-item");
        let starImage = document.createElement('img');
        if (i <= rating) {
            starImage.src = '/static/image/reviews/star_yellow.svg';
            starImage.alt = 'желтая звезда';
        } else {
            starImage.src = '/static/image/reviews/star_grey.svg';
            starImage.alt = 'серая звезда';
        }
        starsItem.appendChild(starImage);
        starsList.appendChild(starsItem);
    }

    const images = response.review_images
    const caruselModal = document.querySelector('.carusel-modal');

    for (let i = 0; i < images.length; i++) {
        let imageContainer = document.createElement('div');
        imageContainer.classList.add("image-container");

        let image = document.createElement('img');
        let src = images[i][0]
        image.src = '/' + String(src);
        image.alt = 'Фото курорта';

        imageContainer.appendChild(image);
        caruselModal.appendChild(imageContainer);
    }
     //modal.classList.add("open");
}

function getReviewEditModalContent(response) {

    const modal = document.getElementById('modal-edit-review');

    const form = document.querySelector('.form__editing_review');

    const nameElement = modal.querySelector('.review-resort-name');
    nameElement.textContent = response.resort_name;

    const regionElement = modal.querySelector('.review-resort-region');
    regionElement.textContent = response.resort_region;
  
    const textElement = modal.querySelector('.form__text');
    textElement.textContent = response.review_text;

    const rating = response.review_rating;
    const starsList = document.querySelector('.stars');

    const button = document.querySelector('.form__button');
    button.id = response.review_id;


    for (let i = 1; i <= 5; i++) {
        let starsItem = document.createElement('input');
        starsItem.classList.add("get_value");
        starsItem.type = "radio"
        starsItem.name = "rating"
        starsItem.value = i

        if (i <= rating) {
            starsItem.classList.add("get_value2");
            starsItem.classList.remove("get_value");
          }

        starsList.appendChild(starsItem);
    }

    const fotoContainer = modal.querySelector('.foto-container');
    const images = response.review_images;
    console.log(images)


    if(images.length > 0) {

        for (let i = 0; i < images.length; i++) {

            let previewImage = document.createElement('div');
            previewImage.classList.add('preview-image')

            let image = document.createElement('img');
            let src = images[i][0]
            image.src = '/' + String(src);
            image.alt = getFileName(String(src));

            let previewRemove = document.createElement('div');
            previewRemove.classList.add('preview-remove');
            previewRemove.setAttribute('data-name', getFileName(String(src)));
            previewRemove.innerHTML = '&times;';

            let previewInfo = document.createElement('div');
            previewInfo.classList.add('preview-info')
    
            previewImage.appendChild(previewRemove);
            previewImage.appendChild(image);
            previewImage.appendChild(previewInfo);

            fotoContainer.appendChild(previewImage);
        }
    }


}

function getFileName(url) {
  const regex = /\/([^\/]+\.jpg)$/i;
  const result = url.match(regex);

  if (result) {
    return result[1];
  } else {
    return 'Файл не найден';
  }
}

function getReview(id) {
    clearModalContent();
    var modal = document.getElementById('modal-review-full');
    openModal(modal);
    origin = location.origin;
    $.ajax({
        url: origin + "/resorts/get_review/" + id + "/", // путь к обработчику на сервере
        type: "GET",

        // обработка успешного ответа
        success: function(response) {
            console.log(response);
            getReviewModalContent(response);
        }
    });
}

function getEditReview(id) {
    clearModalContent();
    var modal = document.getElementById('modal-edit-review');
    openModal(modal);
    origin = location.origin;
    $.ajax({
        url: origin + "/resorts/get_review/" + id + "/", // путь к обработчику на сервере
        type: "GET",

        // обработка успешного ответа
        success: function(response) {
            getReviewEditModalContent(response);
        }
    });
}