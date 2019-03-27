$(function () {
    $("#confirm").click(function () {


        var pic1 = document.getElementsByTagName("input");
        var pic2 = document.getElementsByTagName("select");
        var pic3 = document.getElementsByTagName("textarea");
        var title = pic1[0].value;
        var people = pic1[1].value;
        var time = pic1[2].value;
        var budget = pic1[3].value;
        var location = pic1[4].value;
        var content = pic3[0].value;
        var category = pic2[0].value

        // console.log(title);
        // console.log(content);
        // console.log(people);
        // console.log(time);
        // console.log(budget);
        // console.log(location);
        // console.log(category);
        $.post('./post', {
          title,
          people,
          time,
          budget,
          location,
          content,
          category
        }, function (msg) {
          if(msg.user=='fail')
          {
            alert(msg.msg)
          }
          else {
            $('.content').hide();
            $("#clear").show();

            window.setTimeout(function(){window.location.href = "./post";},2000);

          }

        }, "json");
        // location.href = "/";
    });

    $("#cancel").click(function () {
        location.href = "/";
    });
})
