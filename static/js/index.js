$(function () {
    $("#recommended>div").html([
        "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3506901399,170737939&fm=26&gp=0.jpg",
        "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1484117707,233613571&fm=26&gp=0.jpg",
        "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2488425760,3791675756&fm=26&gp=0.jpg",
        "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3005883822,2867182496&fm=26&gp=0.jpg",
        "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1379292423,1577183614&fm=26&gp=0.jpg"
    ].map(v => `<div class="rec_img" style="background-image:url('${v}')"></div>`))

    // $("#lobby").html(["asd", "asd", "asd"].map(v => `<div>${v}</div>`))
    ("#lobby").html([].map(v => `<div>${v}</div>`))
})