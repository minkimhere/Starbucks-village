function sign_out() {
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃!')
    window.location.href = "/login"
}

function sortCoffee(selected) {
    $('.category_nav > ul > li').removeClass()
    $(selected).parent('li').addClass('selected')
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
        },
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    });
}

function toggleLike(reviewId, checklike) {
    event.stopPropagation()
    console.log(reviewId)
    console.log(checklike)
    let likeButton = $(`#${reviewId}`);
    likeButton.siblings('.like-num').empty()
    $('.left-content > .like > span').empty()
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
                $('.left-content > .like > .like-button').addClass("unlike-button").removeClass("like-button")
                let like_num = response['result_like']['Like']
                likeButton.siblings('.like-num').append(like_num)
                $('.left-content > .like > span').append(like_num)
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
                $('.left-content > .like > .unlike-button').addClass("like-button").removeClass("unlike-button")
                let like_num = response['result_like']['Like']
                likeButton.siblings('.like-num').append(like_num)
                $('.left-content > .like > span').append(like_num)
            }
        })
    }


}

$(function(){
    $('.card').on('click',function(e){
        if(!$(e.target).hasClass('star')){
            $('.modal-box-content').empty()
            let id = $(this).find('.like').children('button').attr('id')
            console.log(id)
            $.ajax({
                type: 'POST',
                url: '/api/modal',
                data: {
                    id_give: id
                },
                success: function (response) {
                    let card = response['card']
                    let name = card['coffeeName']
                    let category = card['category']
                    let img = card['image']
                    let nickname = card['nickname']
                    let review = card['review']
                    let star = card['starRating']
                    let id = card['_id']
                    let like = card['Like']
                    let checkLike = card['heart_by_me']
                    let delete_auth = response['delete_auth']

                    let temp_html = `<div class="left-content">
                                        <figure class="image image is-1by1">
                                            <img src="${img}" alt="${name}">
                                        </figure>
                                        <div class="like">                                  
                                            <span>${like}</span>
                                        </div>
                                    </div>
                                    <div class="right-content">
                                        <p class="title is-3">${name} <span class="delete_auth"><i class="fas fa-trash-alt"></i></span></p>
                                        <p class="subtitle is-6">${category}</p>
                                        <figure class="image is-3by1 star">
                                            <img src="../static/img/star${star}.svg" alt="${star}점">
                                        </figure>
                                        <div class="modal-review-content">
                                            ${review}
                                        </div>                               
                                        <div class="nickname">
                                            <p>by. ${nickname}</p>
                                        </div>
                                    </div>`
                    $('.modal-box-content').append(temp_html)
                    if(checkLike == true){
                        $('.left-content > .like').prepend(`<button id="${id}" class="unlike-button" onclick="toggleLike('${id}')"></button>`)
                    } else if(checkLike == false){
                        $('.left-content > .like').prepend(`<button id="${id}" class="like-button" onclick="toggleLike('${id}')"></button>`)
                    }
                    if(delete_auth == false){
                        $('.right-content > .title > span').removeClass('delete_auth')
                    }
                }
            })
            $('.modal-post').show()
            let value_top = window.innerHeight / 2 - $('.modal-content').outerHeight() / 2
            $('.modal-content').css({'top': value_top})
        }

    })

    $('.modal-post-background,.delete').on('click',function(){
        $('.modal-post').hide()
    })
})