// Видимость пароля при переключении глазка
const btnPass = document.querySelectorAll('.js-btn-password');

btnPass.forEach(function (btn) {
    btn.onclick = function () {
        let target = this.getAttribute('data-target');
        let inputPass = document.querySelector(target);

        if (inputPass.getAttribute('type') === 'password') {
            inputPass.setAttribute('type', 'text');
            btn.classList.add('active');
        } else {
            inputPass.setAttribute('type', 'password');
            btn.classList.remove('active');
        }
        return false;
    }
});

// Переключение между вкладками вход и регистрация в модальном окне
const loginForm = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");

signupBtn.onclick = (()=>{
  loginForm.style.marginLeft = "-50%";
});
loginBtn.onclick = (()=>{
  loginForm.style.marginLeft = "0%";
});


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

// Клик на кнопку забыли пароль
document.getElementById("forgot-password-btn").addEventListener("click", function() {
    document.getElementById("modal-signup-signin").classList.remove("open")
    document.getElementById("modal-account-recovery").classList.add("open")
});


/*------Модальное окно удаление аккаунта-----*/

// Открыть модальное окно удаления аккаунта

//const modals = document.querySelectorAll('.modal');
//const modalBtnsClose = document.querySelectorAll('.js-btn-modal-close');

//document.getElementById("btn-delete-account").addEventListener("click", function() {
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



//document.getElementById("submit-btn-account-recovery").addEventListener("click", function() {
//    document.getElementById("modal-account-recovery").classList.remove("open")
//    document.getElementById("modal-account-recovery__send-message").classList.add("open")
//});

//document.getElementById("main2").addEventListener("click", function() {
//    document.getElementById("modal-account-recovery__send-message").classList.remove("open")
//    document.getElementById("modal-new-password").classList.add("open")
//});

//document.getElementById("change-password").addEventListener("click", function() {
//    document.getElementById("modal-new-password").classList.remove("open")
//    document.getElementById("password-changed").classList.add("open")
//});