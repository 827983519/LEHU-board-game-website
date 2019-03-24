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
        toggle()
    })
})