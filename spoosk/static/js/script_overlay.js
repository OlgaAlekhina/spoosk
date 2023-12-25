const modals = Array.from(document.querySelectorAll('.modal'));
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
  modal.classList.add("open");
  toggleScrollLock();
}

function closeModal(modal) {
    modal.classList.remove("open");
    toggleScrollLock();
    resetForms();
}

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

// Привязка обработчика события "click" для кнопки "Подробнее" на карточке отзыва
if (document.getElementById("open-modal-review-full")) {
    document.getElementById("open-modal-review-full").addEventListener("click", function() {
        openModal(document.getElementById("modal-review-full"))
    });
}

closeModalBtns.forEach((btn, i) => {
    btn.addEventListener("click", function () {
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

// Открыть модальное окно удаления аккаунта
if (document.getElementById("btn-delete-account")) {
document.getElementById("btn-delete-account").addEventListener("click", function() {
    openModal(document.getElementById("modal-account-delete"))
});
}