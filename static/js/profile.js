$(function () {
    function toggle() {
        $("#edit").toggle();
        $("#save").toggle();
        $("#cancel").toggle();
        $("#change_photo").toggle();
        $("#upload_photo").toggle();
        $(".field>.value").toggle();
        $(".field>.input").toggle();
    }

    $("#edit").click(function () {
    var a = document.getElementById("favourite123").innerHTML.split(';');
    document.getElementById("favourite1").value= a[0];
    document.getElementById("favourite2").value= a[1];
    document.getElementById("favourite3").value= a[2];
    toggle();
});

    $("#upload_photo").change(function(){
      var reads = new FileReader();
      f = document.getElementById('upload_photo').files[0];
      reads.readAsDataURL(f);
      reads.onload = function(e) {
      document.getElementById('photo').src = this.result;
    }
    });


    //$("#cancel").click(toggle);

    $("#cancel").click(function (){
      window.location.href = "./profile";


    });

    $("#save").click(function () {

        let nickname = $.trim($("#nickname").val()),
            bio = $.trim($("#bio").val()),
            email = $.trim($("#email").val()),
            cellphone = $.trim($("#cellphone").val()),
            province = $.trim($("#province").val()),
            city = $.trim($("#city").val()),
            favourite1 = $.trim($("#favourite1").val()),
            favourite2 = $.trim($("#favourite2").val()),
            favourite3 = $.trim($("#favourite3").val());

            var photo = document.getElementById("upload_photo").files[0];

            var formData=new FormData();
            formData.append('photo',photo);
            formData.append('nickname',nickname);
            formData.append('bio',bio);
            formData.append('email',email);
            formData.append('cellphone',cellphone);
            formData.append('province',province);
            formData.append('city',city);
            formData.append('favourite1',favourite1);
            formData.append('favourite2',favourite2);
            formData.append('favourite3',favourite3);

        $.ajax({
          url:"./profile",
          type:"POST",
          data:formData,
          dataType:"JSON",
          cache:false,
          contentType:false,
          processData:false
        }).done(function(ret){
          window.location.href = "./profile";
        });
});
})

/*    $("#save").click(function () {

        let nickname = $.trim($("#nickname").val()),
            bio = $.trim($("#bio").val()),
            email = $.trim($("#email").val()),
            cellphone = $.trim($("#cellphone").val()),
            province = $.trim($("#province").val()),
            city = $.trim($("#city").val()),
            favourite1 = $.trim($("#favourite1").val()),
            favourite2 = $.trim($("#favourite2").val()),
            favourite3 = $.trim($("#favourite3").val());

            var photo = document.getElementById("upload_photo").files[0];
            var formData=new FormData();
            formData.append('photo',photo);

        $.post('./profile',{
            nickname,
            bio,
            email,
            cellphone,
            city,
            province,
            favourite1,
            favourite2,
            favourite3,
            formData,
        },function (msg) {
          window.location.href = "./profile";
        }, "json");
});*/
/*  function createSelect(){
    var mySelect = document.createElement("select");
    mySelect.id = "mySelect";
  //  mySelect.style.position = "absolute"
    //mySelect.style.height= 100;
    //mySelecct.style.cssText="height: 18px;width: 100%;  border-radius: 18px;"
    document.body.appendChild(mySelect);
  }*/

//  $('#add_game').click(createSelect);

  //$("#edit").click(toggle);
