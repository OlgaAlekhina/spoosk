const modals = Array.from(document.querySelectorAll('.modal'));
const closeModalBtns = Array.from(document.querySelectorAll('.modal__close-btn'));

function resetForms() {
    document.getElementById("login-form").reset();
    document.getElementById("signup-form").reset();
    document.getElementById("reset-request").reset();
    document.getElementById("reset-form").reset();
    document.getElementById('signup-response').innerHTML = "";
    document.getElementById('results').innerHTML = "";
    document.getElementById('reset_results').innerHTML = "";
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

if (document.querySelector(".modal .form-register__box")) {
  element.addEventListener('click', function (event) {
    event._isClickWithInModal = true;
  });
}

if (document.querySelector(".modal .form-register__box-rec")) {
  element.addEventListener('click', function (event) {
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
document.getElementById("btn-delete-account").addEventListener("click", function() {
    document.getElementById("modal-account-delete").classList.add("open")
});
