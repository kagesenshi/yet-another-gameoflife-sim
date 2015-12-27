// Put your JS here
var chart = dc.heatMap("#gol-grid")
d3.json("/golsession/1.json", function (data) {
    var ndx = crossfilter(data);
    var dim = ndx.dimension(function (d) { return [d.x,d.y] });
    var group = dim.group().reduceSum(function (d) {
        return d.val;   
    });

    chart.options({
        width: 1024,
        height:1024,
        dimension: dim,
        group: group,
        keyAccessor: function (d) {
            return d.key[0]
        },
        valueAccessor: function (d) {
            return d.key[1]
        },
        colorAccessor: function (d) {
            return d.value
        },
        colors: ['#FFF','#000'],
        boxOnClick: function (d) {}
    });

    chart.xBorderRadius(0);
    chart.yBorderRadius(0);

    chart.render();
});
