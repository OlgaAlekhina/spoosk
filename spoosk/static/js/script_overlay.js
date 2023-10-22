// Привязка обработчика события "click" для кнопки "Профиль", открытия модального окна авторизации/регистрации
document.getElementById("open-modal-profile-btn").addEventListener("click", function() {
    document.getElementById("modal-signup-signin").classList.add("open")
});

// Получение всех элементов с классом "modal"
const modals = document.querySelectorAll('.modal');

// Получение всех элементов с классом "modal__close-btn"
const btnCloseModal = document.querySelectorAll('.modal__close-btn');

for (let i = 0; i < btnCloseModal.length; i++) {
  // Привязка обработчика события "click" для каждой кнопки крестика
  btnCloseModal[i].addEventListener("click", function() {
    // Закрытие модального окна
    modals[i].classList.remove("open")
  });

  // Обработчик события "click" для удаления класса "open" модального окна при нажатии вне окна
  document.querySelector(".modal .form-register__box").addEventListener('click', event => {
    event._isClickWithInModal = true;
  });

  modals[i].addEventListener("click", event => {
    if (event._isClickWithInModal) return
    event.currentTarget.classList.remove('open');
  });
}

// Обработчик события "keydown" для удаления класса "open" модального окна при нажатии на клавишу Esc
document.addEventListener("keydown", function(event) {
  if (event.key === "Escape") {
    for (let i = 0; i < modals.length; i++) {
      const modal = modals[i];

      if (modal.classList.contains("open")) {
        // Удаление класса "open" для закрытия модального окна
        modal.classList.remove("open");
        break;
      }
    }
  }
});



// Открыть модальное окно удаления аккаунта
document.getElementById("btn-delete-account").addEventListener("click", function() {
    document.getElementById("modal-account-delete").classList.add("open")
});






// Открыть модальное окно добавления отзывов
// document.getElementById("open-modal-review").addEventListener("click", function() {
//     document.getElementById("modal-add-review").classList.add("open")
// });
// Закрыть модальное окно добавления отзывов
//document.getElementById("close-modal-add-review").addEventListener("click", function() {
//    document.getElementById("modal-add-review").classList.remove("open")
//});
// Закрыть модальное окно при нажатии на Esc
//window.addEventListener('keydown', (e) => {
//    if (e.key === "Escape") {
//        document.getElementById("modal-add-review").classList.remove("open")
//    }
//});
// Закрыть модальное окно при клике вне его
// document.querySelector("#modal-add-review .modal-add-review__box").addEventListener('click', event => {
//     event._isClickWithInModal = true;
// });
// document.getElementById("modal-add-review").addEventListener('click', event => {
//     if (event._isClickWithInModal) return;
//     event.currentTarget.classList.remove('open');
// });

// Открыть модальное окно сравнения
//document.getElementById("open-modal-comparison-btn").addEventListener("click", function() {
//    document.getElementById("my-modal-comparison").classList.add("open")
//})

// Закрыть модальное окно сравнения при клике вне его
//document.querySelector("#my-modal-comparison .modal-comparison_box").addEventListener('click', event => {
//    event._isClickWithInModal = true;
//});
//document.getElementById("my-modal-comparison").addEventListener('click', event => {
//    if (event._isClickWithInModal) return;
//    event.currentTarget.classList.remove('open');
//});

// Открыть модальное окно
// document.getElementById("open-modal-btn").addEventListener("click", function() {
//     document.getElementById("my-modal").classList.add("open")
// })

// Закрыть модальное окно
// document.getElementById("close-my-modal-btn").addEventListener("click", function() {
//     document.getElementById("my-modal").classList.remove("open")
// })

// Закрыть модальное окно при нажатии на Esc
//window.addEventListener('keydown', (e) => {
//    if (e.key === "Escape") {
//        document.getElementById("my-modal").classList.remove("open")
//    }
//});

// Закрыть модальное окно при клике вне его
// document.querySelector("#my-modal .modal_box").addEventListener('click', event => {
//     event._isClickWithInModal = true;
// });
// document.getElementById("my-modal").addEventListener('click', event => {
//     if (event._isClickWithInModal) return;
//     event.currentTarget.classList.remove('open');
// });

