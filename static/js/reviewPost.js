function closePost() {
    if ($(".review-post").css("display") == "block") {
        $(".review-post").hide();
        $(".close-button").text("열기");
    }
}

function getCategory(selected) {
    $("#coffee-name").empty();

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