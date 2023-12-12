$(function () {
    // Initialize datepicker
    $("#entryDate").datepicker();
    $("#exitDate").datepicker();
});

function submitReservation() {
    // Get form data
    const entryDate = new Date($("#entryDate").val());
    const exitDate = new Date($("#exitDate").val());
    const numberOfPeople = $("#numberOfPeople").val();
    const roomType = $("#roomType").val();
    const ordererName = $("#ordererName").val();
    const ordererEmail = $("#ordererEmail").val();
    const ordererPhoneNumber = $("#ordererPhoneNumber").val();
    const metodePembayaran = $("#metodePembayaran").val();
    let harga = 0

    let jumlah_hari = (exitDate - entryDate) / (24 * 60 * 60 * 1000)


// tryy

    if (roomType == 'standard') {
        harga = 2000 * jumlah_hari
    }
    else {
        harga = 17000 * jumlah_hari
    }


    var options = { weekday: 'short', month: 'short', day: 'numeric', year:'numeric' };
    var formattedEntryDate = entryDate.toLocaleDateString('en-US', options);
    var formattedExitDate = exitDate.toLocaleDateString('en-US', options);

    var resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
    <div class="title">
                        <p>Your Stay</p>
                    </div>
                    <div class="res-content" >
                        <div class="kiri">
                            <div class="fill">
                                <h3>Nama</h3>
                                <p>${ordererName}</p>
                            </div>
                            <div class="fill">
                                <h3>Check In</h3>
                                <p>${formattedEntryDate}</p>
                            </div>
                            <div class="fill">
                                <h3>Room</h3>
                                <p>${roomType}</p>
                            </div>
                        </div>
                        <div class="kanan">
                            <div class="fill">
                                <h3>Email</h3>
                                <p>${ordererEmail}</p>
                            </div>
                            <div class="fill">
                                <h3>Check Out</h3>
                                <p>${formattedExitDate}</p>
                            </div>
                            <div class="fill">
                                <h3>Payment Method</h3>
                                <p>${metodePembayaran}</p>
                            </div>
                        </div>
                    </div>
                    <div class="time">
                        <div class="ket">
                            <p>${formattedEntryDate} - ${formattedExitDate}</p>
                            <p>${numberOfPeople} People</p>
                            <p class="fw fs-5">Total Price: ${harga}
                        </div>
                        <div class="save-btn">
                            <button class="btn-booknow" onclick="booking()">Book Now</button>
                        </div>
                    </div>
    `

    var ringkasanDiv = document.querySelector('.ringkasan');
    ringkasanDiv.style.display = 'block';


    var saveBtn = document.querySelector('.save-btn');
    saveBtn.style.display = 'none';
}

function booking() {
    const entryDate = new Date($("#entryDate").val());
    const exitDate = new Date($("#exitDate").val());
    const numberOfPeople = $("#numberOfPeople").val();
    const roomType = $("#roomType").val();
    const ordererName = $("#ordererName").val();
    const ordererEmail = $("#ordererEmail").val();
    const ordererPhoneNumber = $("#ordererPhoneNumber").val();
    const metodePembayaran = $("#metodePembayaran").val();
    let harga = 0

    let jumlah_hari = (exitDate - entryDate) / (24 * 60 * 60 * 1000)






    if (roomType == 'standard') {
        harga = 2000 * jumlah_hari
    }
    else {
        harga = 17000 * jumlah_hari
    }


    $.ajax({
        type: "POST",
        url: "/submit_reservation",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify({
            entryDate,
            exitDate,
            numberOfPeople,
            roomType,
            ordererName,
            ordererEmail,
            ordererPhoneNumber,
            metodePembayaran,
            harga,
            jumlah_hari
        }),
        dataType: "json",
        success: function (response) {
            alert("Reservation successful!");
        },
        error: function (error) {
            alert("Error submitting reservation. Please try again.");
        },
    });
}