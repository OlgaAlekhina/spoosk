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

signupBtn.onclick = (() => {
  loginForm.style.marginLeft = "-50%";
});
loginBtn.onclick = (() => {
  loginForm.style.marginLeft = "0%";
});

// Клик на кнопку забыли пароль
document.getElementById("forgot-password-btn").addEventListener("click", function() {
    document.getElementById("modal-signup-signin").classList.remove("open")
    document.getElementById("modal-account-recovery").classList.add("open")
});
