
try:
    import usocket as socket
except:
    import socket

import gc


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


function addData(data) {
    $.each(data, function(index, value) {        
        tempPoints.push({x: index, y: value.temp});
        humidPoints.push({x: index, y: value.humid});
        heightPoints.push({x: index, y: value.height});

        
    });
    chart1.render();
    chart2.render();
    chart3.render();
}


function updateData() {
    $.getJSON("testData.json", addData)
}
updateData();

var chartT = new Highcharts.Chart({
  chart:{ renderTo : 'chart-temperature-hi' },
  title: { text: 'Temperature' },
  series: [{
    showInLegend: false,
    data: tempPoints
  }],
  plotOptions: {
    line: { animation: false,
      dataLabels: { enabled: true }
    },
    series: { color: '#059e8a' }
  }
});

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
<div id="chart-temperature-hi" style="height: 230px; width: 100%;"></div>
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