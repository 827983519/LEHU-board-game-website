$("#signup").click(function (e) {
    e.preventDefault();
    window.location.href = "./register.html";
});

$("#login").click(function (e) {
    e.preventDefault();
    let username = $.trim($("#username").val()),
        password = $.trim($("#password").val());
    if (!username) {
        alert("User name is required.");
        return;
    }
    if (!password) {
        alert("Password is required");
        return;
    }
    $.post('./login', {
        username,
        password
    }, function (msg) {
        if (msg.user === 'success') {
            window.location.href = "./";
        } else {
            //alert("User name or password is wrong.");
            $('#message').html(msg.msg);
        }
    }, "json");
});
