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

// get rating from review form
var star_rating = 0;
$(".get_value").click(function () {
    if($(this).prop("checked")) {
        star_rating = $(this).val();
        $("#rating_value").val(star_rating);
    }
});

// Review submit
$('#adding_review').on('submit', function(event){
    
    const ratingValue = document.querySelector('input[id="rating_value"]').value;
    console.log(ratingValue)
    if (ratingValue < 1) {
        alert('Оцените курорт');
        event.preventDefault();
    } else {
        event.preventDefault();
        review_submit();
        const modal = document.getElementById('modal-add-review');
        closeModal(modal);

    }
});

// AJAX for review submit
function review_submit() {
    origin = location.origin;
    var form_data = new FormData();
    form_data.append('text', $('#id_text').val());
    form_data.append('id_resort', $('#id_resort').val());
    form_data.append('rating', $('#rating_value').val());
    for(var i = 0; i < file_list.length; i++){
        var file = file_list[i];
        form_data.append('images', file);
    }
    $.ajax({
        url : origin + "/review_submit/", // the endpoint
        type : "POST", // http method
        processData: false,
        contentType: false,
        cache: false,
        data: form_data,
        enctype: 'multipart/form-data',

        // handle a successful response
        success : function(json) {
            console.log('success');
        },
    });
};

// функция для изменения цвета range input в зависимости от текущего значения
$.fn.rangeColor = function(){
    value = ($(this).val()-$(this).prop('min'))/($(this).prop('max')-$(this).prop('min'))*100;
    $(this).css('background', 'linear-gradient(to right, #005FF9 0%, #005FF9 ' + value + '%, #7CB8FF ' + value + '%, #7CB8FF 100%)');
}

// меняет цвет range input во всплывающем фильтре на главной странице
$(".slider").on('input', $.fn.rangeColor);

// call AJAX to pass parameters to advanced filter
$('.filter-submit').on('click', function(event){
    event.preventDefault();
	const region = document.getElementById("region").value;
	const month = document.getElementById("month").value;
	const level = document.getElementById("level").value;
    const green_trails = document.getElementById("easy");
    const blue_trails = document.getElementById("medium");
	const red_trails = document.getElementById("increased-complexity");
	const black_trails = document.getElementById("difficult");
	const freeride = document.getElementById("freeride");
	const snowpark = document.getElementById("snowpark");
	const bygel = document.getElementById("bygel");
	const chairlifts = document.getElementById("chairlifts");
	const gandola = document.getElementById("gandola");
	const travelators = document.getElementById("travelators");
	const adults = document.getElementById("adults");
	const children = document.getElementById("children");
    const distance = document.getElementById("distance").value;
    const rent = document.getElementById("rent");
    const skating = document.getElementById("skating");
	var jsonData = {};
	if (region != 'Все регионы' && region != ''){jsonData['resort_region'] = region;}
	if (month != 'Не важно' && month != ''){jsonData['resort_month'] = month;}
	if (level === 'Ученик'){jsonData['resort_level'] = 'green';}
	if (level === 'Новичок'){jsonData['resort_level'] = 'blue';}
	if (level === 'Опытный'){jsonData['resort_level'] = 'red';}
	if (level === 'Экстремал'){jsonData['resort_level'] = 'black';}
	if (green_trails.checked){jsonData['have_green_skitrails'] = 'green';}
	if (blue_trails.checked){jsonData['have_blue_skitrails'] = 'blue';}
	if (red_trails.checked){jsonData['have_red_skitrails'] = 'red';}
	if (black_trails.checked){jsonData['have_black_skitrails'] = 'black';}
	if (freeride.checked){jsonData['have_freeride'] = '1';}
	if (snowpark.checked){jsonData['have_snowpark'] = '1';}
	if (bygel.checked){jsonData['have_bugelny'] = '1';}
	if (chairlifts.checked){jsonData['have_armchair'] = '1';}
	if (gandola.checked){jsonData['have_gondola'] = '1';}
	if (travelators.checked){jsonData['have_travelators'] = '1';}
	if (adults.checked){jsonData['have_adult_school'] = '1';}
	if (children.checked){jsonData['have_children_school'] = '1';}
	if (distance === '0'){jsonData['airport_distance'] = '50';}
	if (distance === '100'){jsonData['airport_distance'] = '100';}
	if (rent.checked){jsonData['have_rental'] = '1';}
	if (skating.checked){jsonData['have_evening_skiing'] = '1';}
    get_filter(jsonData);
});

// AJAX for advanced resorts filter
function get_filter(jsonData) {
    origin = location.origin;
    url = origin + "/resorts/filter/";
    $.ajax({
            url : url,
            type : "GET",
            data : jsonData,

            success : function(response) {
                $(".page-banner").addClass("page_filters-banner");
                $(".change-logo").html("<img src='/static/image/header/logo_blue.png' alt='Logo' width='190' height='57'>");
                $("#tags").removeClass("search-input-white").addClass("search-input-blue");
                $(".search-btn").addClass("menu-link-blue").html("<img src='/static/image/header/header_search_icon_blue.svg' alt='Поиск' width='28' height='28'><div class='name'>Поиск</div>");
                $("#open-modal-comparison-btn").addClass("menu-link-blue").html("<img src='/static/image/header/header_comparison_icon_blue.svg' alt='Поиск' width='28' height='28'><div class='name'>Сравнить</div>");
                $("#open-modal-profile-btn").addClass("menu-link-blue").html("<img src='/static/image/header/header_account_icon_blue.svg' alt='Поиск' width='28' height='28'><div class='name'>Профиль</div>");
                $(".remove-elem").remove();
                $(".banner-image").html("<img src='/static/image/header/_sport_.png' alt ='Горы' class='img-filters-banner'>");
                $(".page-cards").html(response);
                $(".page-reviews").remove();
                $("#modal-advanced-filters").removeClass("open");
                $("#modal-advanced-filters").html("");
                $("body").removeClass('no-scroll');
                $("body").removeAttr("style");
                $(".search-slider").rangeColor();
                $(".search-slider").on('input', $.fn.rangeColor);
            },
        });
};

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
    const password_pattern = /^[a-zA-Z0-9!#.$%&+=?^_`{|}~-]{2,}$/;
    if (password.length < 8) {
        throw 'Пароль должен содержать не менее 8 символов';
    }
    else if (!password_pattern.test(password)) {
        throw 'Пароль содержит недопустимые символы';
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
    try {
        validatePassword(password);
    } catch (e) {
        document.getElementById('signup-response').innerHTML="<strong>" + e + "</strong>";
    }
    var validate_password = validatePassword(password);
    document.getElementById('signup-response').innerHTML="";
    if (validate_email === true && validate_password === true) {
        user_signup();
    }
});

// AJAX for signup
function user_signup() {
    origin = location.origin;
    $.ajax({
        url : origin + "/signup_endpoint/", // the endpoint
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
    origin = location.origin;
    $.ajax({
        url : origin + "/login_endpoint/", // the endpoint
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

// AJAX for google auth
//function googleLogin() {
//    $.ajax({
//        url : "../google-login", // the endpoint
//        type : "GET", // http method
////        crossDomain: true,
//
//        // handle a successful response
//        success : function() {
//            console.log('success login with google account');
//        },
//
//        // handle a non-successful response
//        error : function() {
//            console.log('error');
////            $('#google-results').html("<strong>"+json.responseJSON.error+
////                "</strong>"); // add the error to the dom
//        }
//    });
//};


// Reset password request submit
$('#reset-request').on('submit', function(event){
    event.preventDefault();
    reset_request();
});

// AJAX for reset password request
function reset_request() {
    origin = location.origin;
    $.ajax({
        url : origin + "/reset_request/", // the endpoint
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
            $('#modal-new-password').removeClass("open");
            $('#modal-password-changed').addClass("open");
            console.log("success");
        },

        // handle a non-successful response
        error : function(json) {
            console.log("error");
        }
    });
};

// AJAX for add/remove resort to/from favorites
function addtoFavorites(id_resort) {
    favorites_id = "favorites-" + id_resort;
    origin = location.origin;
    $.ajax({
        url : origin + "/add_resort/" + id_resort + "/", // the endpoint
        type : "GET", // http method

        // handle a successful response
        success : function(data) {
            button = $("#" + favorites_id);
            if (data.action === 'delete') {
                $('#resort-favorites-text').html("Добавить <br>в избранное");
                if (button.hasClass("favorites-btn")) {
                    button.removeClass("favorites-btn");
                    button.addClass("btn-white");
                }
                if (button.hasClass("resort-btn-favorites")) {
                    button.removeClass("resort-btn-favorites");
                    button.addClass("resort-btn");
                }
            }
            else {
                $('#resort-favorites-text').html("Добавлено <br>в избранное");
                if (button.hasClass("btn-white")) {
                    button.removeClass("btn-white");
                    button.addClass("favorites-btn");
                }
                if (button.hasClass("resort-btn")) {
                    button.removeClass("resort-btn");
                    button.addClass("resort-btn-favorites");
                }
            }
        },
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

