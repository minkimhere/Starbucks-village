function sortCoffee(selected) {
    if (selected == "모두보기") {
        $(`#review-card`).addClass('review-open')
    } else {
        $(`#review-card`).addClass('review-close')
    }
}



$(function(){

    $('.card').on('click',function(){
        $('.modal-box-content').empty()
        let id = $(this).find('input').attr('id')
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

                let temp_html = `<div class="left-content">
                                    <figure class="image image is-1by1">
                                        <img src="${img}" alt="${name}">
                                    </figure>
                                    <div class="like">
                                        <input id="${id}" type="checkbox">
                                        <label for="${id}" class="unchecked"></label>
                                        <label for="${id}">${like}</label>
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
            }
        })
        $('.modal-post').show()
        let value_top = window.innerHeight / 2 - $('.modal-content').outerHeight() / 2
        $('.modal-content').css({'top': value_top})
    })

    $('.modal-post-background,.delete').on('click',function(){
        $('.modal-post').hide()
    })
})