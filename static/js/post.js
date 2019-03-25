$(function () {
    $(".input.time>select:nth-child(1)").html(
        `<option value="" disabled selected hidden>[MM]</option>
        ${"0".repeat(12)
            .split("")
            .map((v,k)=>`<option value="${k+1}">${k+1}</option>`)
        }`
    );

    $(".input.time>select:nth-child(1)").change(function (e) {
        let date = new Date();
        date.setMonth(e.target.value);
        date.setDate(0);
        // get avaliable date by Date
        $(".input.time>select:nth-child(2)").html(
            `<option value="" disabled selected hidden>[MM]</option>
            ${"0".repeat(date.getDate())
                .split("")
                .map((v,k)=>`<option value="${k+1}">${k+1}</option>`)
            }`
        )
    });

    $(".input.time>select:nth-child(3)").html(
        `<option value="" disabled selected hidden>[MM]</option>
        ${"0".repeat(24)
            .split("")
            .map((v,k)=>`<option value="${k+1}">${k+1}</option>`)
        }`
    );

    $("#seek").click(function () {
        $("#seek").removeClass("unselected");
        $("#offer").addClass("unselected");
    });

    $("#offer").click(function () {
        $("#offer").removeClass("unselected");
        $("#seek").addClass("unselected");
    });

    $("#confirm").click(function () {
        $('.content').hide();
        $("#clear").show();
    });

    $("#cancel").click(function () {
        location.href = "index.html";
    });
})