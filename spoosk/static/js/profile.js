// add avatar preview before loading to DB
var loadFile = function(event) {
    var user_ava = document.getElementById('user_ava');
    var avatar = document.getElementById('avatar');
    console.log(avatar.files[0]);
    user_ava.src = URL.createObjectURL(event.target.files[0]);
    user_ava.onload = function() {
        URL.revokeObjectURL(user_ava.src) // free memory
    }
};
