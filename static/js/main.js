function sign_out() {
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃!')
    window.location.href = "/login"
}

function sortCoffee(selected) {
    let select = $(selected).text()
    console.log(select)
    if (select == "모두보기") {
        $(`.card`).css('display', 'block');
    }
    else if (select == "주스(병음료)") {
        $(`.card`).css('display', 'none');
        $(`.주스`).css('display', 'block');
    }
    else if (select == "콜드 브루") {
        $(`.card`).css('display', 'none');
        $(`.콜드`).css('display', 'block');
    }
    else {
        $(`.card`).css('display', 'none');
        $(`.${select}`).css('display', 'block');
    }
}

function closePost() {
    if ($(".review-post").css("display") == "block") {
        $(".review-post").hide();
        $(".close-button").text("열기");
    }
}

function getCategory(selected) {
    $("#coffee-name-select").empty();

    $.ajax({
        type: 'POST',
        url: '/api/category',
        data: {select_give: selected},
        success: function (response) {
            let coffees = response['all_coffees'];
            console.log(coffees);
            for (let i = 0; i < coffees.length; i++) {
                let coffeeName = coffees[i]['coffeeName'];

                let temp_html = `
                            <option value="${coffeeName}">${coffeeName}</option>
                        `;

                $('#coffee-name-select').append(temp_html);
            }
        }
    });
}

function reviewWrite() {
    let category = $('#coffee-category-select option:selected').val();
    let coffeeName = $('#coffee-name-select option:selected').val();
    let starRating = $('#star-rating-select option:selected').val();
    let reviewContent = $('#review-content').val();

    $.ajax({
        type: 'POST',
        url: '/api/write',
        data: {
            category_give: category,
            coffeeName_give: coffeeName,
            starRating_give: starRating,
            review_give: reviewContent,
            nickname_give: 'nickname'
        },
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    });
}

function toggleLike(reviewId, checklike) {
    console.log(reviewId)
    console.log(checklike)
    let likeButton = $(`#${reviewId}`);
    if (likeButton.hasClass("like-button")) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                review_id_give: reviewId,
                action_give: "like"
            },
            success: function (response) {
                likeButton.addClass("unlike-button").removeClass("like-button")
            }
        })
    } else if (likeButton.hasClass("unlike-button")) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                review_id_give: reviewId,
                action_give: "unlike"
            },
            success: function (response) {
                likeButton.addClass("like-button").removeClass("unlike-button")
            }
        })
    }
}