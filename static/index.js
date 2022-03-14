$(document).ready(function () {
    if (top.location.pathname === '/') {
        $.get("http://167.71.214.79:5000/api/order", function (data) {
            setActiveOrder(data);
        });

        let appendTens = document.getElementById("tens")
        let appendSeconds = document.getElementById("seconds")
        let appendMinutes = document.getElementById("minutes")
        let actionLabel = document.getElementById("action")

        let intervalFn;
        let startTime;
        let tilesList;
        let userRecordsList = [];
        let cursor;

        function updateTilesList() {
            // Retrieve the list of tiles
            $.get("http://167.71.214.79:5000/api/tiles", function (data) {
                tilesList = data;
                cursor = 0;
            });
        }

        function resetTimer() {
            clearInterval(intervalFn);
            appendTens.innerHTML = "00";
            appendSeconds.innerHTML = "00";
            appendMinutes.innerHTML = "00";
        }

        function startTimer() {
            startTime = new Date().getTime();
            intervalFn = setInterval(updateTime, 100);
        }

        updateTilesList();

        $("#start-next-btn").click(function (e) {
            if (cursor === tilesList.length) {
                $(this).prop('disabled', true);
                $("#start-next-btn").html("Done!");
            }

            if (cursor < tilesList.length) {
                if (cursor === 0) {
                    $("#start-next-btn").html("Next");
                }

                resetTimer();
                actionLabel.innerHTML = tilesList[cursor].name
                cursor++;
                startTimer()
            }

            if (cursor === tilesList.length) {
                $("#start-next-btn").html("Save");
            }
        });

        $("#restart-btn").click(function () {
            updateTilesList();
            resetTimer();
            $("#start-next-btn").html("Start");
            $("#action").html("[Select this action]");
        });


        function updateTime() {
            let currentTime = new Date().getTime()
            let diff = currentTime - startTime;

            let minutes = Math.floor((diff / 60000)).toString().padStart(2, '0');
            let seconds = Math.floor((diff / 1000) % 60).toString().padStart(2, '0');
            let tens = Math.floor((diff % 1000) / 10).toString().padStart(2, '0');

            appendMinutes.innerHTML = minutes;
            appendSeconds.innerHTML = seconds;
            appendTens.innerHTML = tens;
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
                url: "http://167.71.214.79:5000/api/order",
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
            if(toSelect === selected) {
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


        })
    }
});