
try:
    import usocket as socket
except:
    import socket

import gc
from time import sleep
import network


def connectWifi(ssid='CableBox-BF58', psk='ymn5gzm5um'):
    
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, psk)
    
    for a in range(10):
        if station.isconnected():
            print('Connection successful')
            print(station.ifconfig())
            return True
        
        sleep(1)

    return False

connectWifi()
gc.collect()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

def web_page():  
    html = """
<!DOCTYPE HTML>
<html>
<head>
<script src="https://code.highcharts.com/highcharts.js"></script>
<script>

window.onload = function() {

var tempPoints = [];
var humidPoints = [];
var heightPoints = [];

loadJSON(function(response) {
    //var actual_JSON = JSON.parse(response);
	var actual_JSON = response;
	addData2(actual_JSON);
 });

function loadJSON(callback) {   

	var xobj = new XMLHttpRequest();
		xobj.overrideMimeType("application/json");
	xobj.open('GET', 'testData.json', true);
	xobj.onreadystatechange = function () {
		if (xobj.readyState == 4 && xobj.status == "200") {
			callback(xobj.responseText);
		}
	};
	xobj.send(null);  
}


function addData2(data) {
    $.each(data, function(index, value) {        
        tempPoints.push({x: index, y: value.temp});
        humidPoints.push({x: index, y: value.humid});
        heightPoints.push({x: index, y: value.height});        
    });
    chart1.render();
    chart2.render();
    chart3.render();
}


var chart1 = new CanvasJS.Chart("chart-temperature", {
	theme: "light2",
	title: {
		text: "Temperature"
	},
	data: [{
		type: "line",
		dataPoints: tempPoints
	}]
});

var chart2 = new CanvasJS.Chart("chart-humidity", {
	theme: "light2",
	title: {
		text: "Humidity"
	},
	data: [{
		type: "line",
		dataPoints: humidPoints
	}]
});

var chart3 = new CanvasJS.Chart("chart-height", {
	theme: "light2",
	title: {
		text: "Height"
	},
	data: [{
		type: "line",
		dataPoints: heightPoints
	}]
});

}
</script>
</head>
<body>
<div id="chart-temperature" style="height: 230px; width: 100%;"></div>
<div id="chart-humidity" style="height: 230px; width: 100%;"></div>
<div id="chart-height" style="height: 230px; width: 100%;"></div>

<script src="https://canvasjs.com/assets/script/jquery-1.11.1.min.js"></script>
<script src="https://canvasjs.com/assets/script/jquery.canvasjs.min.js"></script>
</body>
</html>
"""

    return html


def webpageJob():
    while True:
        try:
            if gc.mem_free() < 102000:
                gc.collect()
            conn, addr = s.accept()
            conn.settimeout(3.0)
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            conn.settimeout(None)
            request = str(request)
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()

        except OSError as e:
            conn.close()    
            print ("Connection closed")