// Открыть модальное окно добавления отзывов
document.getElementById("open-modal-review").addEventListener("click", function() {
    document.getElementById("modal-add-review").classList.add("open")
})
// Закрыть модальное окно добавления отзывов
document.getElementById("close-modal-add-review").addEventListener("click", function() {
    document.getElementById("modal-add-review").classList.remove("open")
})
// Закрыть модальное окно при нажатии на Esc
window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("modal-add-review").classList.remove("open")
    }
});
// Закрыть модальное окно при клике вне его
document.querySelector("#modal-add-review .modal-add-review__box").addEventListener('click', event => {
    event._isClickWithInModal = true;
});
document.getElementById("modal-add-review").addEventListener('click', event => {
    if (event._isClickWithInModal) return;
    event.currentTarget.classList.remove('open');
});




// Открыть модальное окно сравнения
document.getElementById("open-modal-comparison-btn").addEventListener("click", function() {
    document.getElementById("my-modal-comparison").classList.add("open")
})

// Закрыть модальное окно сравнения при клике вне его
document.querySelector("#my-modal-comparison .modal-comparison_box").addEventListener('click', event => {
    event._isClickWithInModal = true;
});
document.getElementById("my-modal-comparison").addEventListener('click', event => {
    if (event._isClickWithInModal) return;
    event.currentTarget.classList.remove('open');
});

// Открыть модальное окно
document.getElementById("open-modal-btn").addEventListener("click", function() {
    document.getElementById("my-modal").classList.add("open")
})

// Закрыть модальное окно
document.getElementById("close-my-modal-btn").addEventListener("click", function() {
    document.getElementById("my-modal").classList.remove("open")
})

// Закрыть модальное окно при нажатии на Esc
window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("my-modal").classList.remove("open")
    }
});

// Закрыть модальное окно при клике вне его
document.querySelector("#my-modal .modal_box").addEventListener('click', event => {
    event._isClickWithInModal = true;
});
document.getElementById("my-modal").addEventListener('click', event => {
    if (event._isClickWithInModal) return;
    event.currentTarget.classList.remove('open');
});


