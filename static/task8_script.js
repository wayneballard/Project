// Function to fetch data and update the DOM
function loadData() {
  $.get("/data", function(response) {
    $("#sensor-data").empty();
    $("#sensor-data").append($("<div>").text("Temperature: " + response.temperature + " °C"));
    $("#sensor-data").append($("<div>").text("Humidity: " + response.humidity + " %"));
    $("#sensor-data").append($("<div>").text("Pressure: " + response.pressure + " hPa"));
  });
}

$(document).ready(function() {
  loadData(); // load on startup

  $("#refresh-btn").click(function() {
    loadData();
  });

  // auto-refresh every 5s
  setInterval(loadData, 5000);
});
