let labels = ["Very Low", "Low", "Medium", "High", "Very High"]
let usageChartColor = []

$('#list-tab a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
})

$("input[id^='slider_']").each(function () {
    let default_v = 3
    $(this).val(default_v);
    $(`#${this.id.replace('slider', 'val')}`).html(labels[default_v - 1])
    $(`#${this.id}`).on('input', function (e) {
        $(`#${this.id.replace('slider', 'val')}`).html(labels[$(this).val() - 1]);
    });
});

$("#list-usage-list").click(function(){
    $.get("http://167.71.214.79:5000/tiles", function (data) {
        $.get("http://167.71.214.79:5000/api/frequencies", function (frequencies) {
            let xValues = []
            let yValues = []
            let barColors = [];
            
            data.forEach(function (tile, index) {
                xValues.push(tile.name)
                yValues.push(frequencies[index])
                barColors.push(usageChartColor[index])
            })

            drawUsageChart(xValues, yValues, barColors);
        });
    });
});

$("#list-tile-list").click(function(){
    renderTiles()
});

$("#list-preferences-list").click(function(){
    updateSliderValues()
});

$("#icon-size-slider").slider({
    range: true,
    min: 20,
    max: 50,
    step: 5,
    values: [30, 35],
    slide: function (event, ui) {
        $("#icon-size-value").html(`[${ui.values[0]}, ${ui.values[1]}]`);
        renderTiles()
    }
});

$("#text-size-slider").slider({
    range: true,
    min: 15,
    max: 30,
    step: 5,
    values: [20, 25],
    slide: function (event, ui) {
        $("#text-size-value").html(`[${ui.values[0]}, ${ui.values[1]}]`);
        renderTiles()
    }
});

$("#text-size-value").html(`[${$("#text-size-slider").slider("values", 0)}, ${$("#text-size-slider").slider("values", 1)}]`)
$("#icon-size-value").html(`[${$("#icon-size-slider").slider("values", 0)}, ${$("#icon-size-slider").slider("values", 1)}]`)

$("#apply-btn").click(function (e) {
    let preferences = []
    $("input[id^='slider_']").each(function () {
        // preferences[this.id.replace('slider_', '')] = $(this).val()
        preferences.push($(this).val())    
    });

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: "http://167.71.214.79:5000/api/preferences",
        data: JSON.stringify(preferences),
        dataType : 'json',
        success : (response) => {
            console.log(response)
        },
        error : (err) => {
            console.log(err)
        }
    });
});

function updateSliderValues(){
    $.get("http://167.71.214.79:5000/api/preferences", function (data) {
        $("input[id^='slider_']").each(function (index) {
            console.log(index, this.id)
            $(this).val(data[index]);
            $(`#${this.id.replace('slider', 'val')}`).html(labels[data[index] - 1])
            
        });
    });
}


function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min);
}

function drawUsageChart(xValues, yValues, barColors) {
    let template = '<canvas id="usage-chart" style="width: 100%;"></canvas>'
    
    $('#usage-chart').remove();
    $('#chart-container').append(template);
  
    new Chart("usage-chart", {
        type: "bar",
        data: {
            labels: xValues,
            datasets: [{
                backgroundColor: barColors,
                data: yValues
            }]
        },
        options: {
            legend: {display: false},
            title: {
                display: true,
                text: "No. of Clicks"
            }
        }
    });
}


function renderTiles(){
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: "http://167.71.214.79:5000/tiles",
        dataType : 'json',
        data : JSON.stringify({
            textSizeMin: $("#text-size-slider").slider("values", 0),
            textSizeMax: $("#text-size-slider").slider("values", 1),
            iconSizeMin: $("#icon-size-slider").slider("values", 0),
            iconSizeMax: $("#icon-size-slider").slider("values", 1)
        }),
        success : (data) => {
            console.log(data.solutions)
            htmlLines = ""
            data.solutions.forEach(function(solution, index){
                if (index % 2 == 0) {
                    htmlLines += '<div class="row">'
                }
                htmlLines += `<div class="col tile m-1 tile-func" data-font=${solution.text_size} data-icon=${solution.icon_size}>`
                htmlLines += '<div class="row mt-lg-3">'
                htmlLines += '<div class="col text-center">'
                htmlLines += `<i class="bi bi-stopwatch" style="font-size: ${solution.icon_size}px;"></i>`
                htmlLines += '</div>'
                htmlLines += '</div>'
                htmlLines += '<div class="row mt-1">'
                htmlLines += '<div class="col text-center">'
                htmlLines += `<p style="font-size: ${solution.text_size}px;">Spending Time</p>`
                htmlLines += '</div>'
                htmlLines += '</div>'
                htmlLines += '</div>'
                
                if (index % 2 == 1) {
                    htmlLines += '</div>'
                }
            })
            $('#tile-space').html(htmlLines)
            
            $(".tile-func").click(function(e){
                $(".tile-func").css('background-color', '#2980b9')
                $(this).css('background-color', '#3498db')

                $.ajax({
                    type: 'POST',
                    contentType: 'application/json',
                    url: "http://167.71.214.79:5000/tiles/save",
                    dataType : 'json',
                    data : JSON.stringify({
                        textSize: $(this).attr('data-font'),
                        iconSize: $(this).attr('data-icon')
                    }),
                    success : (data) => {
                        console.log(data)
                    },
                    error : (err) => {
                        console.log(err)
                    }
                });
            })
        },
        error : (err) => {
            console.log(err)
        }
    });
}

$("#randomize-btn").click(function (e) {
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: "http://167.71.214.79:5000/api/frequencies",
        dataType : 'json',
        success : (frequencies) => {
            $.get("http://167.71.214.79:5000/tiles", function (data) {
                let xValues = []
                let yValues = []
                let barColors = [];
                
                data.forEach(function (tile, index) {
                    xValues.push(tile.name)
                    yValues.push(frequencies[index])
                    barColors.push(usageChartColor[index])
                })

                drawUsageChart(xValues, yValues, barColors);
            });
        },
        error : (err) => {
            console.log(err)
        }
    });
});

$(document).ready(function(){
    if (top.location.pathname === '/customize'){
        for (let i = 0; i < 20; i++) {  
            usageChartColor.push(`rgb(${getRandomInt(0, 255)},${getRandomInt(0, 255)},${getRandomInt(0, 255)})`)
        }
    
        updateSliderValues()
    }
});