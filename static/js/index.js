$(function () {
  $("#refresh").click(function (){

     $.post('./refresh', {
     }, function (msg) {
       var pic1 = document.getElementById("pic1");
       var pic2 = document.getElementById("pic2");
       var pic3 = document.getElementById("pic3");
       var pic4 = document.getElementById("pic4");

      document.getElementById("intro1").innerText = msg[0].Store_name+'\n'+msg[0].Location
      document.getElementById("intro2").innerText = msg[1].Store_name+'\n'+msg[1].Location
      document.getElementById("intro3").innerText = msg[2].Store_name+'\n'+msg[2].Location
      document.getElementById("intro4").innerText = msg[3].Store_name+'\n'+msg[3].Location

       pic1.href="http://" +msg[0].Website;
       pic2.href="http://" +msg[1].Website;
       pic3.href="http://" +msg[2].Website;
       pic4.href="http://" +msg[3].Website;

       pic1.children[0].src = "/static/media/" + msg[0].Picture;
       pic2.children[0].src = "/static/media/" + msg[1].Picture;
       pic3.children[0].src = "/static/media/" + msg[2].Picture;
       pic4.children[0].src = "/static/media/" + msg[3].Picture;

     }, "json");
    });

    $("#refresh_activity").click(function (){
      $.post('./', {
      }, function (msg) {
        var pic1 = document.getElementById("lobby").getElementsByTagName("div")
        // console.log(pic1);
        for(i=0;i<pic1.length;i++)
        {
          pic1[i].style.display="none";
          // $(#pic1[i].id).hide()
          }

          for(i=0;i<msg.length;i++)
          {
            var category;
            switch(msg.Category)
          {
           case 1:
           category = 'Card';
           break;
          case 2:
           category = 'Chess';
           case 3:
           category = 'BoardGames';
           break;
          default:
           category = 'Others';
          }
              pic1[i].children[0].innerHTML =  msg[i].start_date+"-" + msg[i].start_time+ '&nbsp;&nbsp;-&nbsp;&nbsp'+ '['+msg[i].activity_title + ']'+ "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"+'Category: '+category + "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"+'Location: '+msg[i].location;
              pic1[i].children[0].href = "/details/" +  msg[i].activity_id + '/register'
              pic1[i].style.display="";


            }


      }, "json");

    });

})
