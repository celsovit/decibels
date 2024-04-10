$(document).ready(function() {
  $.ajax({
    url: "/dashboard/filter-options/",
    type: "GET",
    dataType: "json",
    success: (jsonResponse) => {
      jsonResponse.options.forEach(option => {
        $("#year").append(new Option(option, option));
      });
      loadAllCharts($("#year").children().first().val());
    },
    error: () => console.log("Falha ao obter opções de filtro de gráfico!")
  });

  $("#filterForm").on("submit", (event) => {
    event.preventDefault();
  
    const year = $("#year").val();
    if (year !== null) {
      loadAllCharts(year)
    }
  });
});

function loadChart(chart, endpoint) {
  $.ajax({
    url: endpoint,
    type: "GET",
    dataType: "json",
    success: (jsonResponse) => {

      const title = jsonResponse.title;
      const labels = jsonResponse.data.labels;
      const datasets = jsonResponse.data.datasets;

      // Reset the current chart
      chart.data.datasets = [];
      chart.data.labels = [];

      chart.options.title.text = title;
      chart.options.title.display = true;
      chart.data.labels = labels;
      datasets.forEach(dataset => {
        chart.data.datasets.push(dataset);
      });
      chart.update();
    },
    error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
  });
}

function loadAllCharts(year) {
  if (year === undefined) return;
  loadChart(monthlyAverageChart, `/dashboard/monthly-average/${year}/`);
  loadChart(topPeakWeekdaysChart, `/dashboard/top-peak-weekdays/${year}/`);
  loadChart(topPeakTimesChart, `/dashboard/top-peak-times/${year}/`);
  loadChart(locationsAverageChart, `/dashboard/locations-average/${year}/`);
}
