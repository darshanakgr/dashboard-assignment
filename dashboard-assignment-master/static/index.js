function setActiveOrder(order) {
    if (order == 0) {
        $('#alpha-btn').addClass('active')
        $('#custom-btn').removeClass('active')
    } else {
        $('#alpha-btn').removeClass('active')
        $('#custom-btn').addClass('active')
    }
}


function setOrderBy(order){
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: "http://167.71.214.79:5000/api/order",
        data: JSON.stringify({mode: order}),
        dataType : 'json',
        success : (tiles) => {
            let textSize = $("#menu-space").attr("data-text");
            let iconSize = $("#menu-space").attr("data-icon");
            let htmlLines = ""
            tiles.forEach((tile, index) => {
                if(index % 4 == 0){
                    htmlLines += '<div class="row">'
                }
                    
                htmlLines += '<div class="col tile m-1">'
                htmlLines += '<div class="row mt-lg-3">'
                htmlLines += '<div class="col text-center">'
                htmlLines += `<i class="${tile.icon}" style="font-size: ${iconSize}px;"></i>`
                htmlLines += '</div>'
                htmlLines += '</div>'
                htmlLines += '<div class="row mt-1">'
                htmlLines += '<div class="col text-center">'
                htmlLines += `<p style="font-size: ${textSize}px;">${tile.name}</p>`
                htmlLines += '</div>'
                htmlLines += '</div>'
                htmlLines += '</div>'
                
                if (index % 4 == 3) {
                    htmlLines += '</div>'
                }
            });
            $('#menu-space').html(htmlLines)

            setActiveOrder(order);
        },
        error : (err) => {
            console.log(err);
        }
    });
    
}


$("#alpha-btn").click(function (e) {
    setOrderBy(0)
});

$("#custom-btn").click(function (e) {
    setOrderBy(1)
});

$(document).ready(function(){
    if (top.location.pathname === '/'){
        $.get("http://167.71.214.79:5000/api/order", function(data) {
            setActiveOrder(data);
        });
    }   
});