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
                <div class="col-lg-4 mb-4">
                <div class="card">
                  <img src="${file}" class="img-room">
                  <div class="content d-flex justify-content-between align-items-end">
                    <div class="desc">
                      <h4 class="fw-bold">${Name}</h4>
                      <div class="text-price">
                      <p class="card-price">Rp ${Price}</p>
                      <p class="card-price-desc">/Night/Room</p>
                      </div>
                      <div class="rating">
                        <i class="fa-solid fa-star text-warning"></i>
                        <i class="fa-solid fa-star text-warning"></i>
                        <i class="fa-solid fa-star text-warning"></i>
                        <i class="fa-solid fa-star text-warning"></i>
                        <i class="fa-solid fa-star text-warning"></i>
                        <p style="font-weight:bold">4,7</p>
                      </div>
                    </div>
                    <div>
                      <button class="btn-booknow">Book Now</button>
                    </div>
                  </div>
                </div>
              </div>
                `;
            }

            $("#table-body").html(temp_html);
        },
    });
}