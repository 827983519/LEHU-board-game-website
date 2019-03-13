$(function () {
    $("#history").click(function () {
        location.href = "/history";
    });

    $("#allmessage").click(function () {
        location.href = "/allmessage";
    });
/*
  $(".single_activity").click(function () {
     var adom = document.getElementsByClassName('invisible');
        console.log(adom[0].id[0])

      //  a = "/sadsadasd"
      //  location.href = a;
    });
    */
	$(".message").click(function () {
        location.href = "event.html";
    });


    function changeURL(activity_id) {
      var a = 'details/' + activity_id;
      location.href = a;
    };



})
