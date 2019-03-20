$(function () {

$("#signup").click(function (e) {
     e.preventDefault();

    let username = $.trim($("#username").val()),
        password = $.trim($("#password").val()),
        confirmPassword = $.trim($("#confirmPassword").val()),
        email = $.trim($("#email").val()),
        gender = $.trim($("#gender").val());
        var agree = document.getElementById("agree");


    if (!username || !password || !confirmPassword || !email) {
        alert("Please fill in all the information.");
        return;
    }

    if (agree.checked === false){
    alert("You need to agree to LEHU policy.");
    return;
    }

    $.post('./register', {
        username,
        password,
        confirmPassword,
        email,
        gender
    }, function (msg) {
        if (msg.register === 'success') {
            // window.location.href = "./login";
            alert("Sucess!! Login now!");
            var start = (new Date()).getTime();
            while ((new Date()).getTime() - start < 1000) {
                continue;
              }
              window.location.href = "./login";


        } else {
          alert(msg.msg);
          // (msg.valid_data.username)? document.getElementById("username").value=msg.valid_data.username:document.getElementById("username").value="",
          // (msg.valid_data.password)? document.getElementById("password").value=msg.valid_data.password:document.getElementById("password").value="",
          // (msg.valid_data.confirmPassword)? document.getElementById("confirmPassword").value=msg.valid_data.confirmPassword:document.getElementById("confirmPassword").value="",
          // (msg.valid_data.email)? document.getElementById("email").value=msg.valid_data.email:document.getElementById("email").value="",
          // (msg.valid_data.gender)? document.getElementById("gender").value=msg.valid_data.gender:document.getElementById("gender").value="";
        }
    }, "json");
});
})
