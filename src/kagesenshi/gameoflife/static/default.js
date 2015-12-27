// Put your JS here
var chart = dc.scatterPlot("#gol-grid")
var liveCountDisplay = dc.numberDisplay('#live-count');
var deadCountDisplay = dc.numberDisplay('#dead-count');

function jsonurl () {
    return '/golsession/' + $('#sessionid').val() + '.json';
};

d3.json(jsonurl(), function (data) {
    var ndx = crossfilter(data);
    var dim = ndx.dimension(function (d) { return [d.x,d.y] });
    var group = dim.group().reduceSum(function (d) {
        return d.val;   
    });

    chart.options({
        width: 500,
        height:500,
        dimension: dim,
        group: group,
        symbol: 'square',
        brushOn: false,
        symbolSize: 5,
        x: d3.scale.linear().domain([0,80])
    });

    var liveDim = ndx.dimension(function (d) {
        return d;
    });

    var liveSum = liveDim.group().reduce(function (p, v) {
        if (v.val) {
            p.live += 1;
        } else {
            p.dead += 1;
        }
        p.total += 1;
        return p;
    }, function (p, v) {
        if (v.val) {
            p.live -= 1;
        } else {
            p.dead -= 1;
        }
        p.total -= 1;
        return p;
    }, function (p, v) {
        return { 'live': 0, 'dead': 0, 'total': 0 }
    })

    liveCountDisplay.options({
        group: liveSum,
        valueAccessor: function (d) {
            return d.value.live;
        },
        formatNumber: function (d) {
            return d3.format('f')(d);
        }
    });


    deadCountDisplay.options({
        group: liveSum,
        valueAccessor: function (d) {
            return d.value.dead;
        },
        formatNumber: function (d) {
            return d3.format('f')(d);
        }
    });

    dc.renderAll();

    function step() {
        d3.json(jsonurl() + '?step=1', function (data) {
            ndx.remove();
            ndx.add(data);
            dc.redrawAll();
        });
    };

    $('#step-button').click(step);

    var tracker = null;
    $('#run-button').click(function () {
        if (tracker == null) {
            tracker = setInterval(step, 1500);
        };
    });

    $('#stop-button').click(function () {
        if (tracker != null) {
            clearInterval(tracker);
        }
        tracker = null;
    });

    $('#new-session').click(function () {
        var d = new Date();
        $('#sessionid').val(d.toISOString());
        step()
    });

});
