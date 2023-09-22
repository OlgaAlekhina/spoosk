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