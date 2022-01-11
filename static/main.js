function sortCoffee(selected) {
    console.log(selected);
    if (selected == "모두보기") {
        $(`.card`).css('display', 'block');
    } else {
        $(`.card`).css('display', 'none');
        $(`.${selected}`).css('display', 'block');
    }
}

function toggle_like(review_id, type) {
    console.log(review_id, type)
    let $a_like = $(`#${review_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like.hasClass("fa-heart"))
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/api/update_like",
            data: {
                post_id_give: review_id,
                type_give: type,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass("fa-heart-o").removeClass("fa-heart")
                $a_like.find("span.like-num").text(response["count"])
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/api/update_like",
            data: {
                post_id_give: review_id,
                type_give: type,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass("fa-heart").removeClass("fa-heart-o")
                $a_like.find("span.like-num").text(response["count"])
            }
        })

    }
}

function deleteReview(review) {
    console.log(review)
    $.ajax({
        type: "POST",
        url: `/api/delete_review`,
        data: {review_give: review},
        success: function (response) {
            alert(response["msg"])
            window.location.href = "/"
        }
    });
}