$(function () {
    $("#history").click(function () {
        location.href = "/history";
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

    $(".content").click(function () {
         var a = getElementById('content').value;
         console.log(a);
          location.href = "event.html";
      });

    function changeURL(activity_id) {
      var a = 'details/' + activity_id;
      location.href = a;
    };



})

function changeURL(activity_id) {
  var a = 'details/' + activity_id;
  location.href = a;
}

function messageURL(user_name) {
    // var a ="a";
    // console.log(a)
    location.href = user_name;
}
