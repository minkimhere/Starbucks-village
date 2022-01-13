// 로그아웃
function sign_out() {
    // 쿠키에 저장되어 있는 토큰 삭제
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃!')
    // 로그아웃이 되면 다시 로그인 페이지로 이동
    window.location.href = "/login"
}

// 카테고리 별 리뷰카드를 보여주기 위한 함수
function sortCoffee(selected) {
    // 클릭되지 않은 카테고리 버튼에 class 삭제
    $('.category_nav > ul > li').removeClass()
    // 클릭된 않은 카테고리 버튼에 class 추가
    $(selected).parent('li').addClass('selected')
    
    // 선택된 카테고리의 text를 select에 저장
    let select = $(selected).text()
    console.log(select)
    // 선택된 카테고리에 따라 리뷰 카드들을 보여주거나 숨김
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

// 리뷰를 작성하기 위해 선택된 카테고리안에 음료들의 서버에서 받아 option태그를 생성
function getCategory(selected) {
    // 이전에 받아온 option 태그들을 삭제
    $("#coffee-name-select").empty();

    $.ajax({
        type: 'POST',
        url: '/api/category',
        // 선택된 카테고리 명을 서버로 전송
        data: {select_give: selected},
        success: function (response) {
            // 서버에서 보내준 카테고리안에 음료의 정보를 받아 저장
            let coffees = response['all_coffees'];
            console.log(coffees);
            // 보내준 정보의 길이 만큼 반복
            for (let i = 0; i < coffees.length; i++) {
                // 보내준 정보 중 커피의 이름만 저장
                let coffeeName = coffees[i]['coffeeName'];
                
                // 커피의 이름을 보여주는 option태그 생성
                let temp_html = `
                            <option value="${coffeeName}">${coffeeName}</option>
                        `;
                // 생성된 태그들을 coffee-name-select id를 가진 태그 안에 생성
                $('#coffee-name-select').append(temp_html);
            }
        }
    });
}

// 사용자가 작성한 리뷰의 내용을 서버로 전달하는 함수
function reviewWrite() {
    // 사용자가 작성한 카테고리, 커피이름, 평점, 리뷰 내용을 받아 저장
    let category = $('#coffee-category-select option:selected').val();
    let coffeeName = $('#coffee-name-select option:selected').val();
    let starRating = $('#star-rating-select option:selected').val();
    let reviewContent = $('#review-content').val();

    $.ajax({
        type: 'POST',
        url: '/api/write',
        data: {
            // 저장된 정보를 서버로 전송
            category_give: category,
            coffeeName_give: coffeeName,
            starRating_give: starRating,
            review_give: reviewContent,
        },
        success: function (response) {
            alert(response['msg']);
            // 작성이 완료되면 페이지 리로드
            window.location.reload()
        }
    });
}

// 로그인된 유저에 따라 like 인지 unlike 인지 확인하여 데이터 전송, 버튼 모양 변경
function toggleLike(reviewId) {
    event.stopPropagation()
    // 클릭한 like 버튼의 reviewId를 선택
    let likeButton = $(`#${reviewId}`);

    //선택된 like 버튼의 내용을 바꾸기 전 내용 삭제
    likeButton.siblings('span').empty()
    $('.left-content > .like > span').empty()

    // 사용자가 아직 like를 누르지 않은 상태라면
    if (likeButton.hasClass("like-button")) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                // 선택한 like의 reviewId와 like를 눌렀다는 것을 서버에 전송
                review_id_give: reviewId,
                action_give: "like"
            },
            success: function (response) {
                // like 버튼에 class 추가, 삭제로 모습과 상태 변경
                likeButton.addClass("unlike-button").removeClass("like-button")
                $('.left-content > .like > .like-button').addClass("unlike-button").removeClass("like-button")
                // like 개수를 서버에서 받음
                let like_num = response['result_like']['Like']
                // liken 버튼에 변경된 좋아요 개수 표시
                likeButton.siblings('span').append(like_num)
                $('.left-content > .like > span').append(like_num)
            }
        })
    } // 사용자가 이미 like를 누른 상태라면
    else if (likeButton.hasClass("unlike-button")) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                // 선택한 unlike의 reviewId와 unlike를 눌렀다는 것을 서버에 전송
                review_id_give: reviewId,
                action_give: "unlike"
            },
            success: function (response) {
                // like 버튼에 class 추가, 삭제로 모습과 상태 변경
                likeButton.addClass("like-button").removeClass("unlike-button")
                $('.left-content > .like > .unlike-button').addClass("like-button").removeClass("unlike-button")
                // like 개수를 서버에서 받음
                let like_num = response['result_like']['Like']
                // liken 버튼에 변경된 좋아요 개수 표시
                likeButton.siblings('span').append(like_num)
                $('.left-content > .like > span').append(like_num)
            }
        })
    }


}

// 리뷰 카드를 클릭했을 때, 모달을 사용하여 리뷰 상세 정보 표시
$(function(){
    $('.card').on('click',function(e){
        // 이전의 모달의 내용을 삭제
        $('.modal-box-content').empty()
            // 사용자에 맞게 like, unlike를 표시하기 위해 id를 저장
            let id = $(this).find('.like').children('button').attr('id')
            $.ajax({
                type: 'POST',
                url: '/api/modal',
                data: {
                    // 저장된 id를 서버로 전송
                    id_give: id
                },
                success: function (response) {
                    // 모달을 그리기 위한 리뷰의 정보들을 서버에서 받아옴
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
                    
                    // 받아온 정보에 맞춰 모달 생성
                    let temp_html = `<div class="left-content">
                                        <figure class="image image is-1by1">
                                            <img src="${img}" alt="${name}">
                                        </figure>
                                        <div class="like">                                  
                                            <span>${like}</span>
                                        </div>
                                    </div>
                                    <div class="right-content">
                                        <p class="title is-3">${name} <span class="delete_auth"><i class="fas fa-trash-alt" onclick="delete_review('${id}')"></i></span></p>
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
                    
                    // 유저의 정보에 따라 like, unlike 버튼을 생성
                    if(checkLike == true){
                        $('.left-content > .like').prepend(`<button id="${id}" class="unlike-button" onclick="toggleLike('${id}')"></button>`)
                    } else if(checkLike == false){
                        $('.left-content > .like').prepend(`<button id="${id}" class="like-button" onclick="toggleLike('${id}')"></button>`)
                    }
                    
                    // 모달이 유저가 작성한 것인지 아닌지에 따라 delete버튼 생성
                    if(delete_auth == false){
                        $('.right-content > .title > span').removeClass('delete_auth')
                    }
                    $('.modal-post').show()
                    let value_top = window.innerHeight / 2 - $('.modal-content').outerHeight() / 2
                    $('.modal-content').css({'top': value_top})
                }
            })
    })
    // 모달 이외의 부분을 클릭했을 경우 모달 사라짐
    $('.modal-post-background,.delete').on('click',function(){
        $('.modal-post').hide()
    })
})

// 리뷰 삭제
function delete_review(reviewId){
    $.ajax({
        type: 'POST',
        url: '/api/delete_review',
        data: {
            // 삭제할 리뷰의 id 값을 받아 서버에 전송
            id_give: reviewId
        },
        success: function(response){
            alert(response['msg'])
            window.location.reload()
        }
    })

}