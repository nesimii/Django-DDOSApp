//websocket bağlantı işlemi
let webSocket;
try {
    webSocket = new WebSocket('ws://' + window.location.host + '/ws/datas/');

} catch (error) {
    toastMessage("web sockete bağlanılamadı", 'red', 0);
}

//web socket bağlantısı açıldığında
webSocket.onopen = function () {
    toastMessage("web socket bağlantısı kuruldu", "green");
};

//web socket bağlantısı kapatılırsa
webSocket.onclose = function () {
    toastMessage("web socket bağlantısı kapatıldı", "red", 0);
};

//websockete bir mesaj gelirse işlemi
webSocket.onmessage = function (e) {
    try {
        let data = JSON.parse(e.data);
        for (key in data['data']) {
            if (data['data'].hasOwnProperty(key)) {
                //console.log("%c " + key + " = " + data['data'][key], "color:green");

                if (key == 'bandwidth') {
                    console.log('bant genişliği: ' + data['data'][key]);

                    var newGraphData = graphData.data.datasets[0].data;
                    newGraphData.shift();
                    newGraphData.push(data['data'][key]);
                    graphData.data.datasets[0].data = newGraphData;
                    myChart.update();

                } else {
                    document.getElementById(key).innerHTML = data['data'][key];
                }
            }
        }
    } catch (error) {
        console.log(error);
    }
};

const ctx = document.getElementById('myChart').getContext('2d');
var graphData = {
    type: 'line',
    data: {
        labels: ['t1', 't2', 't3', 't4', 't5', 't6'],
        datasets: [{
            label: 'Toplam Bant Genişliği (Mb)',
            fontSize: 20,
            data: [0, 0, 0, 0, 0, 0],
            borderColor: 'rgb(46, 160, 80)',
            tension: 0.5,

            borderWidth: 1
        }]
    },
    options: {}
}
const myChart = new Chart(ctx, graphData);

/*
//sockete yeni data geldiğinde charta aktarım yapmak için yapılacak

var newGraphData = graphData.data.datasets[0].data;
newGraphData.shift();
newGraphData.push(djangoData.value);

graphData.data.datasets[0].data = newGraphData;
myChart.update();
*/