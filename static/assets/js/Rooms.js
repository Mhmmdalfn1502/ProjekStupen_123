$(document).ready(function () {
    listing();
    bsCustomFileInput.init();
});

function listing() {
    $.ajax({
        type: "GET",
        url: "/admin",
        data: {},
        success: function (response) {
            console.log(response);
            let articles = response["articles"];
            let temp_html = "";

            for (let i = 0; i < articles.length; i++) {
                let Name = articles[i]["Name"];
                let Price = articles[i]["Price"];
                let file = articles[i]["file"];

                temp_html += `
                    <div class="col-lg-4 col-md-6 col-sm-6" style="width: 18rem;">
                        <img src="${file}" class="card-img-top" alt="...">
                        <div class="card-body">
                            <div class="card-desc">
                                <h5 class="card-name">${Name}</h5>
                                <span class="card-price">Rp. ${Price}</span>
                                <span class="night-room">/Night/Room</span>
                            </div>
                            <div class="rat-btn">
                                <div class="card-rating">
                                    <img class="staricon" src="../static/assets/star.webp" alt="">
                                    <img class="staricon" src="../static/assets/star.webp" alt="">
                                    <img class="staricon" src="../static/assets/star.webp" alt="">
                                    <img class="staricon" src="../static/assets/star.webp" alt="">
                                    <img class="staricon" src="../static/assets/star.webp" alt="">
                                    <span class="review-rating">4.9</span>
                                </div>
                                <a href="#" class="bookbtn">Book now</a>
                            </div>
                        </div>
                    </div>
                `;
            }

            $("#table-body").html(temp_html);
        },
    });
}