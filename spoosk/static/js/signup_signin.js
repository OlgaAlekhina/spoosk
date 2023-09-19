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


const loginForm = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");

signupBtn.onclick = (()=>{
  loginForm.style.marginLeft = "-50%";
});
loginBtn.onclick = (()=>{
  loginForm.style.marginLeft = "0%";
});


// Открыть модальное регистрации/авторизации
document.getElementById("open-modal-profile-btn").addEventListener("click", function() {
    document.getElementById("modal-signup-signin").classList.add("open")
})
// Закрыть модальное окно добавления регистрации/авторизации
document.getElementById("close-modal-profile-btn").addEventListener("click", function() {
    document.getElementById("modal-signup-signin").classList.remove("open")
})
// Закрыть модальное окно при нажатии на Esc
window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("modal-signup-signin").classList.remove("open")
    }
});
// Закрыть модальное окно при клике вне его
document.querySelector("#modal-signup-signin .form-register__box").addEventListener('click', event => {
    event._isClickWithInModal = true;
});
document.getElementById("modal-signup-signin").addEventListener('click', event => {
    if (event._isClickWithInModal) return;
    event.currentTarget.classList.remove('open');
});