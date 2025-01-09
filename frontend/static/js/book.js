document.addEventListener('DOMContentLoaded', () => {
    flight_duration();
});

function flight_duration() {
    document.querySelectorAll(".duration").forEach(element => {
        let time = element.dataset.value.split(":");
        element.innerText = time[0] + "h " + time[1] + "m";
    });
}

function add_traveller() {
    let div = document.querySelector('.add-traveller-div');
    let fname = div.querySelector('#fname');
    let lname = div.querySelector('#lname');
    let gender = div.querySelectorAll('.gender');
    let gender_val = null
    if (fname.value.trim().length === 0) {
        alert("Please enter First Name.");
        return false;
    }

    if (lname.value.trim().length === 0) {
        alert("Please enter Last Name.");
        return false;
    }

    if (!gender[0].checked) {
        if (!gender[1].checked) {
            alert("Please select gender.");
            return false;
        } else {
            gender_val = gender[1].value;
        }
    } else {
        gender_val = gender[0].value;
    }

    let passengerCount = div.parentElement.querySelectorAll(".each-traveller-div .each-traveller").length;

    let traveller = `<div class="row each-traveller">
                        <div>
                            <span class="traveller-name">${fname.value} ${lname.value}</span><span>,</span>
                            <span class="traveller-gender">${gender_val.toUpperCase()}</span>
                        </div>
                        <input type="hidden" name="passenger${passengerCount + 1}FName" value="${fname.value}">
                        <input type="hidden" name="passenger${passengerCount + 1}LName" value="${lname.value}">
                        <input type="hidden" name="passenger${passengerCount + 1}Gender" value="${gender_val}">
                        <div class="delete-traveller">
                            <button class="btn" type="button" onclick="del_traveller(this)">
                                <svg width="1.1em" height="1.1em" viewBox="0 0 16 16" class="bi bi-x-circle" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                    <path fill-rule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                    <path fill-rule="evenodd" d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                                </svg>
                            </button>
                        </div>
                    </div>`;
    div.parentElement.querySelector(".each-traveller-div").innerHTML += traveller;
    div.parentElement.querySelector("#p-count").value = passengerCount + 1;
    div.parentElement.querySelector(".traveller-head h6 span").innerText = passengerCount + 1;
    div.parentElement.querySelector(".no-traveller").style.display = 'none';
    fname.value = "";
    lname.value = "";
    gender.forEach(radio => {
        radio.checked = false;
    });

    let pcount = document.querySelector("#p-count").value;
    let fare = document.querySelector("#basefare").value;
    let fee = document.querySelector("#fee").value;
    if (parseInt(pcount) !== 0) {
        let totalSeatValue = 0;

        // Duyệt qua tất cả các ghế có giá trị và cộng dồn
        document.querySelectorAll('.seat').forEach(seat => {
            if (seat.classList.contains('choose')) { // Chỉ tính ghế được chọn
                const seatId = seat.nextElementSibling.value;
                const seatName = seat.textContent;
                let seatPrice = trip(parseFloat(seat.getAttribute('value')));
                totalSeatValue += seatPrice;
            }
        });
        document.querySelectorAll('.seat1').forEach(seat => {
            if (seat.classList.contains('choose')) { // Chỉ tính ghế được chọn
                const seatId = seat.nextElementSibling.value;
                const seatName = seat.textContent;
                let seatPrice = trip(parseFloat(seat.getAttribute('value')));
                totalSeatValue += seatPrice
            }
        });
        document.querySelector(".base-fare-value span").innerText = parseInt(fare) * parseInt(pcount);
        document.querySelector(".total-fare-value span").innerText = parseInt(totalSeatValue) + (parseInt(fare) * parseInt(pcount)) + parseInt(fee);
    }
}

function del_traveller(btn) {
    let traveller = btn.parentElement.parentElement;
    let tvl = btn.parentElement.parentElement.parentElement.parentElement;
    let cnt = tvl.querySelector("#p-count");
    cnt.value = parseInt(cnt.value) - 1;
    tvl.querySelector(".traveller-head h6 span").innerText = cnt.value;
    if (parseInt(cnt.value) <= 0) {
        tvl.querySelector('.no-traveller').style.display = 'block';
    }
    traveller.remove();

    let pcount = document.querySelector("#p-count").value;
    let fare = document.querySelector("#basefare").value;
    let fee = document.querySelector("#fee").value;
    if (parseInt(pcount) !== 0) {
        document.querySelector(".base-fare-value span").innerText = parseInt(fare) * parseInt(pcount);
        document.querySelector(".total-fare-value span").innerText = (parseInt(fare) * parseInt(pcount)) + parseInt(fee);
    }
}

function book_submit() {
    // Lấy các tham số và đảm bảo tất cả được chuyển đổi thành số
    let pcount = parseInt(document.querySelector("#p-count").value) || 0;
    let people = parseInt(document.getElementById("people").value) || 0;
    let tripType = parseInt(document.getElementById("tripType").value) || 0;
    let seatSelected = parseInt(document.getElementById("chosenCount").value) || 0;
    let seatSelected1 = parseInt(document.getElementById("chosenCount1").value) || 0;
    // Kiểm tra loại chuyến đi (tripType)
    if (tripType === 1) {
        // Loại 1: số ghế phải bằng số người
        if (people !== seatSelected) {
            alert(`Buy enough seat for ${people} people!`);
            return false;
        }
    }
    if (tripType === 2) {
        // Loại 2: số ghế phải bằng số người x 2 (khứ hồi)
        if (people !== seatSelected) {
            alert(`Buy ${people} seat for peoples in flight1!`);
            return false;
        }
        if (people !== seatSelected1) {
            alert(`Buy ${people} seat for peoples in flight2!`);
            return false;
        }
    }

    // Kiểm tra số hành khách phải bằng số người đã chọn
    // if (pcount !== people) {
    //     alert("Please add enough passenger equal your people you chose.");
    //     return false;
    // }
    // Nếu tất cả hợp lệ
    return true;
}



let couponApplied = false; // Flag to track if a coupon has been applied
let couponCodeApplied = ''; // Store the applied coupon code for removal
let percentDiscount = 1; // No discount applied by default

// Utility function to check if today's date is within a given range
function isTodayInRange(startDate, endDate) {
    const today = new Date();
    return today >= new Date(startDate) && today <= new Date(endDate);
}
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length);
        }
    }
    return null;
}


function discount() {
    const couponInput = document.querySelector('input[name="coupon"]');
    const couponCode = couponInput.value.trim();
    var currency = document.getElementById('currency').value;
    // Kiểm tra nếu coupon đã được áp dụng
    if (couponApplied) {
        alert(`Một coupon đã được áp dụng: "${couponCodeApplied}". Vui lòng gỡ bỏ nó trước khi nhập coupon khác.`);
        return;
    }
    function formatVND(value) {
        return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.'); // Thêm dấu chấm
    }

    // Gửi mã coupon đến backend để xác thực
    if (couponCode) {
        $.ajax({
            url: 'http://127.0.0.1:8000/discount/apply-coupon/', // Đường dẫn API
            type: 'POST',
            data: {
                coupon_code: couponCode,
                total_fare: document.querySelector('.total-fare-value span').textContent.trim().replace(/[^\d.-]/g, '')
                , currency: currency
            },
            success: function (data) {
                if (data.error) {
                    alert(data.error);
                    couponInput.value = '';  // Xóa trường nhập
                    return;
                }
                document.getElementById("couponCodeHidden").value = couponCode
                document.getElementById("discountPercentageHidden").value = data.discount
                if (data.currency === 'VND') {
                    // Cập nhật tổng giá trị sau khi giảm giá
                    console.log(data.total_fare);

                    document.querySelector('.total-fare-value span').textContent = ` ${formatVND(parseInt(data.total_fare))}₫`;
                } else {
                    console.log(data.total_fare);

                    document.querySelector('.total-fare-value span').textContent = ` ${parseInt(data.total_fare)} $`;

                }
                // Hiển thị thông tin coupon đã áp dụng
                const couponHtml = `
                        <div class="row surcharges" id="appliedCoupon">
                            <div class="surcharges-label">
                                Coupon: ${data.coupon_code} | Discount: ${data.discount}%
                            </div>
                            <button type="button" class="removeCouponBtn btn btn-danger btn-sm" style="margin-left: 10px;">Gỡ bỏ</button>
                            <input type="hidden" name="coupon" value="${data.coupon_code}">
                        </div>
                    `;
                 const hiddenInput1 = document.createElement("input");
                hiddenInput1.type = "hidden";
                hiddenInput1.name = "coupon";
                hiddenInput1.value = couponCode;

                // Tạo input hidden thứ hai
                const hiddenInput2 = document.createElement("input");
                hiddenInput2.type = "hidden";
                hiddenInput2.name = "session_id";
                hiddenInput2.value = data.discount;
                const surchargesElement = document.querySelector('.surcharges');
                if (surchargesElement) {
                    surchargesElement.insertAdjacentHTML('afterend', couponHtml);
                }

                // Lưu thông tin coupon đã áp dụng
                couponApplied = true;
                couponCodeApplied = data.coupon_code;

                // Vô hiệu hóa trường nhập để ngừng nhập coupon
                couponInput.disabled = true;
                document.querySelector('#applyCoupon').disabled = true;

                // Logic gỡ bỏ coupon
                const removeCouponBtn = document.querySelector('.removeCouponBtn');
                if (removeCouponBtn) {
                    removeCouponBtn.addEventListener('click', function () {
                        // Gỡ bỏ coupon
                        const couponElement = document.querySelector('#appliedCoupon');
                        if (couponElement) {
                            couponElement.remove();
                        }
                        couponApplied = false;
                        couponCodeApplied = '';
                        couponInput.disabled = false;
                        document.querySelector('#applyCoupon').disabled = false;
                        couponInput.value = ''; // Xóa trường nhập
                        updateTotalFare1(data.discount); // Cập nhật lại tổng giá trị sau khi gỡ bỏ coupon
                    });
                }
            },
            error: function (xhr, status, error) {
                // alert('Đã xảy ra lỗi khi áp dụng coupon.');
                console.error(error);
            }
        });
    } else {
        alert('Vui lòng nhập mã coupon hợp lệ.');
    }
}
// Hàm cập nhật tổng tiền sau khi gỡ bỏ coupon
function updateTotalFare1(discount) {
    let totalFare = document.querySelector('.total-fare-value span').textContent.trim().replace(/[^\d.-]/g, '');
    // totalFare = parseInt(totalFare);  // Chuyển sang kiểu số (float)
    var currency = document.getElementById('currency').value;
    // Cập nhật lại tổng tiền, tính lại giá trị ban đầu trước khi giảm giá
    // Để lấy lại giá trị ban đầu trước khi giảm giá, ta cần chia lại tổng số tiền cho phần trăm giảm giá.
    console.log(totalFare.replace(/[^\d-]/g, ''));
    // console.log(originalFare);
    
    
    let originalFare = parseInt(totalFare.replace(/[^\d-]/g, '')) / (1 - discount / 100);
    console.log('1' + totalFare);
    console.log("2" +originalFare);
    
    // Làm tròn giá trị nếu cần
    // originalFare = Math.round(originalFare);  // Làm tròn giá trị để không còn phần thập phân

    // Cập nhật tổng tiền đầy đủ (không có giảm giá)
    if(currency === 'USD') {
    document.querySelector('.total-fare-value span').textContent = `${parseInt(originalFare)} $`; // Cập nhật lại tổng giá trị ban đầu (trước khi giảm giá)

} else  {
    console.log(originalFare);
    document.querySelector('.total-fare-value span').textContent = `${formatVND(  (originalFare))} ₫`; // Cập nhật lại tổng giá trị ban đầu (trước khi giảm giá)

}
}


function trip(price) {
    let tripType = parseInt(document.getElementById("tripType").value) || 0;
    if (tripType === 1) {
        let stop = (document.getElementById("stop").value);
        if (stop === 'yes') {
            return price * 2;
        }
    }
    if (tripType === 2) {
        let stop1 = (document.getElementById("stop1").value);
        if (stop1 === 'yes') {
            return price * 2;
        }
        let stop2 = (document.getElementById("stop2").value);
        if (stop2 === 'yes') {
            return price * 2;
        }
    }
    return price;
}



