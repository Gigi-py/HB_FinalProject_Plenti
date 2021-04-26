
(function () {
config = {
type: 'line',
data: data,
options: {
responsive: true,
plugins: {
    legend: {
    position: 'top',
    },
    title: {
    display: true,
    text: 'Individual Stock Price Chart'
    }
}
},
};

const DATA_COUNT = 7;
const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

const labels = Utils.months({count: 7});
const data = {
labels: ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"],
datasets: [
{
    data: [20, 10, 10, 10, 10, 10, 10],
    borderColor: Utils.CHART_COLORS.red,
    backgroundColor: Utils.transparentize(Utils.CHART_COLORS.red, 0.5),
}
// {
//     label: 'Dataset 2',
//     data: Utils.numbers(NUMBER_CFG),
//     borderColor: Utils.CHART_COLORS.blue,
//     backgroundColor: Utils.transparentize(Utils.CHART_COLORS.blue, 0.5),
// }
]
};
// === include 'setup' then 'config' above ===

var myChart = new Chart(
  document.getElementById('myChart'),
  config
);
