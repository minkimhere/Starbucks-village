function sortCoffee(selected) {
    if (selected == "모두보기") {
        $(`#review-card`).addClass('review-open')
    } else {
        $(`#review-card`).addClass('review-close')
    }
}