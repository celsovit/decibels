const monthlyAverageCtx = document.getElementById("monthlyAverageChart").getContext("2d");
const monthlyAverageChart = new Chart(monthlyAverageCtx, {
  type: "bar",
  options: {
    responsive: true,
    title: {
      display: false,
      text: ""
    }
  }
});
const locationsAverageCtx = document.getElementById("locationsAverageChart").getContext("2d");
const locationsAverageChart = new Chart(locationsAverageCtx, {
  type: "line",
  options: {
    responsive: true,
    title: {
      display: false,
      text: ""
    }
  }
});
const topPeakWeekdaysCtx = document.getElementById("topPeakWeekdaysChart").getContext("2d");
const topPeakWeekdaysChart = new Chart(topPeakWeekdaysCtx, {
  type: "polarArea",
  options: {
    responsive: true,
    maintainAspectRatio: false,
    aspectRatio: 1,
    title: {
      display: true,
      text: "Locações Maiores Índices"
    },
  }
});
const topPeakTimesCtx = document.getElementById("topPeakTimesChart").getContext("2d");
const topPeakTimesChart = new Chart(topPeakTimesCtx, {
  type: "pie",
  options: {
    responsive: true,
    maintainAspectRatio: false,
    aspectRatio: 1,
    title: {
      display: false,
      text: ""
    },
    layout: {
      padding: 15,
    },
    plugins: {
      labels: {
        position: 'outside',
        textMargin: 8,
      },
      datalabels: {
        formatter: (value) => {
          if (value < 3) {
            return '';
          }
        }
      }
    }
  },
  plugins: [ChartDataLabels],
});