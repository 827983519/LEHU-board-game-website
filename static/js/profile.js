$(function () {
    function toggle() {
        $("#edit").toggle();
        $("#save").toggle();
        $("#cancel").toggle();

        $(".field>.value").toggle();
        $(".field>.input").toggle();
    }
    $("#edit").click(toggle);

    $("#cancel").click(toggle);

    $("#save").click(function () {

        let nickname = $.trim($("#nickname").val()),
            bio = $.trim($("#bio").val()),
            email = $.trim($("#email").val()),
            cellphone = $.trim($("#cellphone").val()),
            province = $.trim($("#province").val()),
            city = $.trim($("#city").val());

        $.post('./profile',{
            nickname,
            bio,
            email,
            cellphone,
            city,
            province,
        },function (msg) {
          window.location.href = "./profile";
        }, "json");
});

})
