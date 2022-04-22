$(document).ready(function () {
    if (top.location.pathname === '/') {
        let origin = window.location.origin
        let speechRecognition = window.webkitSpeechRecognition
        let recognition = new speechRecognition()

        recognition.continuous = false

        recognition.onstart = function () {
            $("#voice-cmd-btn").prop('disabled', true);
        }

        recognition.onspeechend = function () {
            $("#voice-cmd-btn").prop('disabled', false);
        }

        recognition.onerror = function () {
            alert("Error with Speech Recognition Engine.")
            $("#voice-cmd-btn").prop('disabled', false);
        }

        recognition.onresult = function (event) {
            let transcript = event.results[event.resultIndex][0].transcript.trim().toLowerCase()
            console.log(`Transcript: ${transcript}`);

            $.ajax({
                url: `${origin}/api/voice`,
                type: "get",
                data: {query: transcript},
                success: function (tile_id) {
                    console.log(`Match: ${tile_id}`);
                    if (tile_id != null) {
                        $('div[data-id="' + tile_id + '"]').css('background-color', '#e74c3c');
                    } else {
                        alert("Unable to recognize the command!. Pls try again.")
                    }

                },
                error: function (error) {
                    console.log(error);
                }
            });
        }

        $("#voice-cmd-btn").click(function (e) {
            recognition.start();
            $(".tile").css('background-color', '#2980b9')
        })
    }
});