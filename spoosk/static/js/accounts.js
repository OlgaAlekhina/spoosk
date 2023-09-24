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

                error : function(json) {
                    window.location = 'http://127.0.0.1:8000/link_expired';
                    console.log("error");
                }
            });
    };

// Signup submit
$('#signup-form').on('submit', function(event){
    event.preventDefault();
    user_signup();
});

// AJAX for signup
function user_signup() {
    $.ajax({
        url : "../signup_endpoint/", // the endpoint
        type : "POST", // http method
        data : { username : $('#username').val(), usermail : $('#usermail').val(), password : $('#login-password').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#usermail').val(''); // remove the value from the input
            $('#login-password').val(''); // remove the value from the input
            $("#signup-response").html("<strong>Check your email to finish registration!");
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
        data : { user_mail : $('#user_mail').val(), login_password : $('#signup-password').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#user_mail').val(''); // remove the value from the input
            $('#signup-password').val(''); // remove the value from the input
            $("#response").html("<strong>Вы успешно авторизовались!</strong>");
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
    change_password();
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
            $('#password-changed').addClass("open")
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