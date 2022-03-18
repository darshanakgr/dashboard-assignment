$(document).ready(function () {
    if (top.location.pathname === '/') {

        let usageChartColor = []

        for (let i = 0; i < 20; i++) {
            usageChartColor.push(`rgb(${getRandomInt(0, 255)},${getRandomInt(0, 255)},${getRandomInt(0, 255)})`)
        }

        function getRandomInt(min, max) {
            min = Math.ceil(min);
            max = Math.floor(max);
            return Math.floor(Math.random() * (max - min) + min);
        }

        function setActiveOrder(order) {
            if (order == 0) {
                $('#alpha-btn').addClass('active')
                $('#custom-btn').removeClass('active')
            } else {
                $('#alpha-btn').removeClass('active')
                $('#custom-btn').addClass('active')
            }
        }

        function setOrderBy(order) {
            $.ajax({
                type: 'POST',
                contentType: 'application/json',
                url: "http://127.0.0.1:5000/api/order",
                data: JSON.stringify({mode: order}),
                dataType: 'json',
                success: (tiles) => {
                    let textSize = $("#menu-space").attr("data-text");
                    let iconSize = $("#menu-space").attr("data-icon");
                    let htmlLines = ""
                    tiles.forEach((tile, index) => {
                        if (index % 4 == 0) {
                            htmlLines += '<div class="row">'
                        }

                        htmlLines += `<div class="col tile m-1 tile-func" data-id="${tile.id}">`
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
                error: (err) => {
                    console.log(err);
                }
            });
        }

        function setVote(vote_value) {
            $.ajax({
                type: 'POST',
                contentType: 'application/json',
                url: "http://127.0.0.1:5000/api/vote",
                data: JSON.stringify({vote: vote_value}),
                dataType: 'json',
                success: (res) => {
                    console.log(res);
                },
                error: (err) => {
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

        $(".tile-func").click(function (e) {
            $(".tile-func").css('background-color', '#2980b9')
            let toSelect = tilesList[cursor - 1].id
            let selected = $(this).attr('data-id');
            if (toSelect === selected) {
                $(this).css('background-color', '#3498db')
                clearInterval(intervalFn);
                let currentTime = new Date().getTime();
                userRecordsList.push({
                    "action": toSelect,
                    "elapsed_time": currentTime - startTime
                })
                console.log(`${toSelect} & ${selected} : ${currentTime - startTime}`)
            } else {
                $(this).css('background-color', '#e74c3c')
            }


        });

        $.get("http://127.0.0.1:5000/api/order", function (data) {
            setActiveOrder(data);
        });

        $.get("http://127.0.0.1:5000/api/vote", function (data) {
            if (data == null) {
                $("#vote-yes").prop("checked", false);
                $("#vote-no").prop("checked", false);
            } else {
                if (data) {
                    $("#vote-yes").prop("checked", true);
                } else {
                    $("#vote-no").prop("checked", true);
                }
            }
        });

        $("#vote-btn").click(function (e) {
            if (!$("#vote-yes").is(":checked") && !$("#vote-no").is(":checked")) {
                alert("Please select your vote before submission!")
            } else {
                setVote($("input[type='radio'][name='vote']:checked").val() === "yes")
            }
        });

        function drawUsageChart(xValues, yValues, barColors, chartId) {
            new Chart(chartId, {
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
                    title: {display: false}
                }
            });
        }

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: "http://127.0.0.1:5000/api/frequencies",
            dataType: 'json',
            success: (frequencies) => {
                $.get("http://127.0.0.1:5000/tiles", function (data) {
                    let xValues = []
                    let yValues = []
                    let barColors = [];

                    data.forEach(function (tile, index) {
                        xValues.push(tile.name)
                        yValues.push(frequencies[index])
                        barColors.push(usageChartColor[index])
                    })

                    drawUsageChart(xValues, yValues, barColors, "usage-chart");
                });
            },
            error: (err) => {
                console.log(err)
            }
        });

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: "http://127.0.0.1:5000/api/preferences",
            dataType: 'json',
            success: (frequencies) => {
                $.get("http://127.0.0.1:5000/tiles", function (data) {
                    let xValues = []
                    let yValues = []
                    let barColors = [];

                    data.forEach(function (tile, index) {
                        xValues.push(tile.name)
                        yValues.push(frequencies[index])
                        barColors.push(usageChartColor[index])
                    })

                    drawUsageChart(xValues, yValues, barColors, "preference-chart");
                });
            },
            error: (err) => {
                console.log(err)
            }
        });
    }
});