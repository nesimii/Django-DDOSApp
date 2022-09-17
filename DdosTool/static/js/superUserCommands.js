function sendCommand() {

    var radios = document.getElementsByName('deviceCommands');
    for (var radio of radios) {
        if (radio.checked) {
            var targetIp = document.getElementById('targetIp').value;
            ajaxSendData('sendCommand', radio.value, targetIp);
        }
    }
}

function cancelCommand() {
    ajaxSendData('cancelCommand');
}

let commandStatus = false;

function ajaxSendData(request, commandId = 0, targetIp = 0) {
    let csrf = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "http://" + window.location.host + "/sshCommand", type: "POST", dataType: 'json', data: {
            csrfmiddlewaretoken: csrf, text: request, commandId: commandId, targetIp: targetIp,
        }, success: function (response) {
            if (response.text) {
                commandStatus = true;
                toastMessage(response.text, "green");
            } else if (response.error) {
                commandStatus = false;
                toastMessage(response.error, "red");
            } else {
                toastMessage('hata oluştu', "orange");
            }
        },
    });
}

