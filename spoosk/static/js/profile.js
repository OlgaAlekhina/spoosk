// add avatar preview before loading to DB
var loadFile = function(event) {
    var user_ava = document.getElementById('user_ava');
    var avatar = document.getElementById('avatar');
    user_ava.src = URL.createObjectURL(event.target.files[0]);
    user_ava.onload = function() {
        URL.revokeObjectURL(user_ava.src) // free memory
    }
};

// delete account on click
$('#overlay-delete-account').on('click', function(event){
    event.preventDefault();
    deleteAccount();
});

// AJAX for delete account
function deleteAccount() {
    user_id = document.getElementById('user_id').innerHTML;

    $.ajax({
        url : "../delete_account/", // the endpoint
        type : "POST", // http method
        data : { user_id : user_id }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#modal-account-delete').removeClass("open")
            $('#modal-account-delete1').addClass("open")
            console.log("success");
        },
    });
};

// AJAX for remove resort from favorites with page reload
function removefromFavorites(id_resort) {
    origin = location.origin;
    $.ajax({
        url : origin + "/add_resort/" + id_resort + "/", // the endpoint
        type : "GET", // http method

        // handle a successful response
        success : function(json) {
            loadFavorites();
        },
    });
};

// AJAX for loading user's favorites
function loadFavorites() {
    $.ajax({
        url : "/favorites/", // the endpoint
        type : "GET", // http method

        // handle a successful response
        success : function(response) {
            $('.menu__item-reviews').removeClass("active")
            $('.menu__link-reviews').removeClass("active")
            $(".editing_profile-container").html(response);
            $('.menu__item-favorites').addClass("active")
            $('.menu__link-favorites').addClass("active")
        },
    });
};

function loadReviews() {
    $.ajax({
        url : "/user_reviews/", // the endpoint
        type : "GET", // http method

        // handle a successful response
        success : function(response) {
            $('.menu__item-favorites').removeClass("active")
            $('.menu__link-favorites').removeClass("active")
            $(".editing_profile-container").html(response);
            $('.menu__item-reviews').addClass("active")
            $('.menu__link-reviews').addClass("active")
        },
    });
};

// Edit review
function editReview(id) {
    origin = location.origin;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var form_data = new FormData();
    form_data.append('text', $('#id_text').val());
    form_data.append('rating', $('#rating_value').val());
    for (var key of form_data.entries()) {
        console.log(key[0] + ', ' + key[1]);
    }
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url : origin + "/edit_review/" + id + "/", // the endpoint
        type : "POST", // http method
        processData: false,
        contentType: false,
        cache: false,
        data: form_data,
        enctype: 'multipart/form-data',

        // handle a successful response
        success : function(json) {
            $('#modal-edit-review').removeClass("open");
            $("body").removeClass('no-scroll').removeAttr("style");
            loadReviews();
        },
    });
};

// Delete review
function deleteReview(id) {
    origin = location.origin;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url : origin + "/delete_review/" + id + "/", // the endpoint
        type : "DELETE", // http method

        // handle a successful response
        success : function(json) {
            console.log('success');
            $("#review-delete-popup-" + id).hide();
            $('#review-' + id).hide();
            number = parseInt($("#review_number").text());
            new_number = number - 1;
            $("#review_number").text(new_number);
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
