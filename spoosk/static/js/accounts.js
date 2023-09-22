// Signup submit
$('#signup-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    user_signup();
});

// AJAX for signup
function user_signup() {
    console.log("user_signup is working!") // sanity check
    $.ajax({
        url : "signup_endpoint", // the endpoint
        type : "POST", // http method
        data : { username : $('#username').val(), usermail : $('#usermail').val(), password : $('#password').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#usermail').val(''); // remove the value from the input
            $('#password').val(''); // remove the value from the input
            console.log(json);
            $("#response").html("<strong>Check your email to finish registration!");
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(json) {
            $('#results').html("<div>"+json.responseJSON.error+
                "</div>"); // add the error to the dom
            console.log(json.status + ": " + json.responseText); // provide a bit more info about the error to the console
        }
    });
};

// Login submit
$('#login-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    user_login();
});

// AJAX for login
function user_login() {
    console.log("user_login is working!") // sanity check
    $.ajax({
        url : "../login_endpoint/", // the endpoint
        type : "POST", // http method
        data : { user_mail : $('#user_mail').val(), login_password : $('#login-password').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#user_mail').val(''); // remove the value from the input
            $('#login-password').val(''); // remove the value from the input
            console.log(json);
            $("#response").html("<strong>Вы успешно авторизовались!</strong>");
            console.log("success"); // another sanity check
            location.reload();
        },

        // handle a non-successful response
        error : function(json) {
            $('#login_results').html("<div>"+json.responseJSON.error+
                "</div>"); // add the error to the dom
            console.log(json.status + ": " + json.responseText); // provide a bit more info about the error to the console
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