// Put your JS here
var svg = dimple.newSvg("#gol-grid", 1024, 1024);
d3.json("/golsession/1.json", function (data) {
  var myChart = new dimple.chart(svg, data);
  myChart.addCategoryAxis("x", "x");
  myChart.addCategoryAxis("y", "y");
  myChart.addSeries("val", dimple.plot.bar);
  myChart.draw();
});
