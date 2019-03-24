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
    
    $("#recommended>div").html([
        "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3506901399,170737939&fm=26&gp=0.jpg",
        "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1484117707,233613571&fm=26&gp=0.jpg",
        "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2488425760,3791675756&fm=26&gp=0.jpg",
        "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3005883822,2867182496&fm=26&gp=0.jpg",
        "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1379292423,1577183614&fm=26&gp=0.jpg"
    ].map(v => `<div class="rec_img" style="background-image:url('${v}')"></div>`))

    $("#lobby").html([{
        host: "host name",
        title: "Title",
        time: "2019-01-02 22:00:00",
        status: "open"
    }].map(v => `<div class="single_activity ${v.status}">
    <span class="host">${v.host}</span>
    <span class="activity_title">[${v.title}]</span>
    <span>${v.time}</span>
    <span class="status"></span>
    </div>`))
})