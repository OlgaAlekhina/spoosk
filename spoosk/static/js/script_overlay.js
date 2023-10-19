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

/*------Модальное окно удаление аккаунта-----*/

// Открыть модальное окно удаления аккаунта

//const modals = document.querySelectorAll('.modal');
//const modalBtnsClose = document.querySelectorAll('.js-btn-modal-close');
//
//document.getElementById("btn-delete-account").ad dEventListener("click", function() {
//    document.getElementById("modal-account-delete").classList.add("open")
//});

//document.getElementById("overlay-delete-account").addEventListener("click", function() {
//   document.getElementById("modal-account-delete").classList.remove("open")
//   document.getElementById("modal-account-delete1").classList.add("open")
//});

//function closeModal(e) {
//    if (e.target.classList.contains('js-btn-modal-close')) {
//        e.target.closest('._modal').classList.remove('open');
//    }
//}
//modals.forEach(modal => {
//    modal.addEventListener('click', e => closeModal(e))
//})

//Array.from(modalBtnsClose, closeButton => {
//    closeButton.addEventListener('click', e => e.target.closest('.modal').classList.remove('open'));
//});

