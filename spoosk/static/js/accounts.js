// check if all input fields of forms are not empty to activate submit button
let get_forms = document.forms;
let forms = Array.from(get_forms);
forms.forEach(form => {
    let get_inputs = form.getElementsByTagName("input");
    let button = form.querySelector("button");
    let inputs = Array.from(get_inputs);
    inputs.forEach(input => {
        input.addEventListener('keyup', () => {
            if (inputs.every(input => input.value)) {
                button.disabled = false;
                button.style.background = "#005FF9";
                button.style.color= "#ffffff";
            }
            else {
                button.disabled = true;
                button.style.background = "#F5F5F7";
                button.style.color= "#B1B2B7";
            }
        })
    })
})

// call AJAX function when url includes token
function get_param() {
        var href = window.location.href;
        var href_split = href.split('?')[1]
        var params = new URLSearchParams(href_split);
        if (params.has('token')) {
            var uidb64 = params.get('uidb64');
            var token = params.get('token');
            reset_confirmation(uidb64, token)
        }
    }
    window.onload = get_param;

// AJAX for auth parameters confirmation
function reset_confirmation(uidb64, token) {
    $.ajax({
            url : "../reset_confirmation/",
            type : "GET",
            data : { uidb64 : uidb64, token : token },

            success : function(data) {
                $('#modal-new-password').addClass("open");
                $('#user_name').val(data.user);
                console.log(data.user);
            },
        });
};

// email validator
function validateEmail(email) {
    const emailRegex = /^([a-zA-Z0-9!#.$%&+=?^_`{|}~-]+@[a-zA-Z0-9.-]+[a-zA-Z0-9]+\.[a-zA-Z]{2,})$/;
    if (!emailRegex.test(email)){
        return false;
    }
    else {
        return true;
    }
}

// password validator
function validatePassword(password) {
    if (password.length < 8) {
        return false;
    }
    else {
        return true;
    }
}

// Signup submit
$('#signup-form').on('submit', function(event){
    event.preventDefault();
    var email = document.getElementById("usermail").value;
    var password = document.getElementById("signup-password").value;
    var validate_email = validateEmail(email);
    if (validate_email === false) {
        document.getElementById('results').innerHTML="<strong>Некорректно введен адрес электронной почты</strong>";
    }
    else {
        document.getElementById('results').innerHTML="";
        }
    var validate_password = validatePassword(password);
    if (validate_password === false) {
        document.getElementById('signup-response').innerHTML="<strong>Пароль должен содержать не менее 8 символов</strong>";
    }
    else {
        document.getElementById('signup-response').innerHTML="";
        }
    if (validate_email === true && validate_password === true) {
        user_signup();
    }
});

// AJAX for signup
function user_signup() {
    $.ajax({
        url : "../signup_endpoint/", // the endpoint
        type : "POST", // http method
        data : { username : $('#username').val(), usermail : $('#usermail').val(), password : $('#signup-password').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#usermail').val(''); // remove the value from the input
            $('#signup-password').val(''); // remove the value from the input
            $('#results').html(''); // remove the previous error
            $("#signup-response").html("<strong>Вам на почту было отправлено письмо для подтверждения регистрации</strong>");
        },

        // handle a non-successful response
        error : function(json) {
            $('#results').html("<strong>"+json.responseJSON.error+
                "</strong>"); // add the error to the dom
        }
    });
};

// Login submit
$('#login-form').on('submit', function(event){
    event.preventDefault();
    user_login();
});

// AJAX for login
function user_login() {
    $.ajax({
        url : "../login_endpoint/", // the endpoint
        type : "POST", // http method
        data : { user_mail : $('#user_mail').val(), login_password : $('#login-password').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#user_mail').val(''); // remove the value from the input
            $('#login-password').val(''); // remove the value from the input
            location.reload();
        },

        // handle a non-successful response
        error : function(json) {
            $('#login_results').html("<strong>"+json.responseJSON.error+
                "</strong>"); // add the error to the dom
        }
    });
};

// Reset password request submit
$('#reset-request').on('submit', function(event){
    event.preventDefault();
    reset_request();
});

// AJAX for reset password request
function reset_request() {
    $.ajax({
        url : "../reset_request/", // the endpoint
        type : "POST", // http method
        data : { user_mail : $('#reset_mail').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#modal-account-recovery').removeClass("open");
            $('#modal-account-recovery__send-message').addClass("open");
            $('#res_mail').html($('#reset_mail').val());
        },

        // handle a non-successful response
        error : function(json) {
            $('#reset_results').html("<strong>"+json.responseJSON.error+
                "</strong>"); // add the error to the dom
        }
    });
};

// Password change submit
$('#reset-form').on('submit', function(event){
    event.preventDefault();
    password1 = document.getElementById("login-password1").value;
    password2 = document.getElementById("new-login-password").value;
    if (password1 != password2) {
        document.getElementById('password_error').innerHTML="<strong>Пароли не совпадают</strong>";
    }
    else {
        change_password();
    }
});

// AJAX for change password
function change_password() {
    $.ajax({
        url : "../reset_endpoint/", // the endpoint
        type : "POST", // http method
        data : { password1 : $('#login-password1').val(), username : $('#user_name').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#modal-new-password').removeClass("open")
            $('#modal-password-changed').addClass("open")
            console.log("success");
        },

        // handle a non-successful response
        error : function(json) {
            console.log("error");
        }
    });
};

// makes forms protected from CSRF
$(function() {

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

