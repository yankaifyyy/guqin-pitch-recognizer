const BadgeName = [
    '岳山',
    '一',
    '二',
    '三',
    '四',
    '五',
    '六',
    '七',
    '八',
    '九',
    '十',
    '十一',
    '十二',
    '十三',
    '龙龈'
];

const BadgePositionRight = [
    0,
    1.0 / 8,
    1.0 / 6,
    1.0 / 5,
    1.0 / 4,
    1.0 / 3,
    2.0 / 5,
    1.0 / 2,
    3.0 / 5,
    2.0 / 3,
    3.0 / 4,
    4.0 / 5,
    5.0 / 6,
    7.0 / 8,
    1.0
];

function initGuqin(svg) {
    const chordWidth = +svg.attr('width');

    // 徽位
    svg.select('g.badges')
        .selectAll('g.badge')
        .data(d3.range(15))
        .enter()
        .append('g')
        .attr('class', 'badge')
        .attr('transform', function(d) {
            var x = (1 - BadgePositionRight[d]) * chordWidth;
            return 'translate(' + x + ', 0)';
        })
        .each(function(d) {
            var text = d;
            d3.select(this)
                .append('circle')
                .attr('r', 7 * (1 + (1 - Math.abs(d - 7) / 7)));
            d3.select(this)
                .append('text')
                .text(BadgeName[d]);
        })

    // 七弦
    const SEP = 15;
    svg.select('g.chords')
        .selectAll('chords')
        .data(d3.range(7))
        .enter()
        .append('line')
        .attr('x1', 0)
        .attr('y1', function(d) {
            return d * SEP;
        })
        .attr('x2', chordWidth)
        .attr('y2', function(d) {
            return d * SEP;
        });
}

function initAxes(svg) {
    const width = +svg.attr('width');
    const height = +svg.attr('height');
    const markerHeight = 15;

    var view = d3.select('g.pos-in-seven');

    // Add chord axis
    view.select('g.axis-x')
        .append('line')
        .attr('class', 'axis')
        .attr('x1', 0)
        .attr('y1', markerHeight)
        .attr('x2', width)
        .attr('y2', markerHeight);
    view.select('g.axis-x')
        .select('g.pos-markers')
        .selectAll('line.marker')
        .data(d3.range(15))
        .enter()
        .append('line')
        .attr('class', 'marker')
        .attr('x1', function(d) {
            return (1 - BadgePositionRight[d]) * width;
        })
        .attr('y1', 0)
        .attr('x2', function(d) {
            return (1 - BadgePositionRight[d]) * width;
        })
        .attr('y2', markerHeight);

    // Add time axis
    view.select('g.axis-y')
        .append('line')
        .attr('class', 'axis')
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('x2', 0)
        .attr('y2', height);
}

function init() {
    var svg = d3.select('svg#view');

    initGuqin(svg);
    initAxes(svg);
}

function visualizeChord7(data) {
    var lines = data.trim().split('\n');
    var points = lines.map(function(line) {
        var vals = line.split('\t');
        var tm = +vals[0];
        var len = +vals[14];
        var pos = vals[15];
        var xy = pos.slice(1, pos.length - 1).split(',');
        var x = +xy[0];
        var y = +xy[1];

        return {
            time: tm,
            len: len,
            x: x,
            y: y
        };
    });

    var maxTime = d3.max(points, function(v) {
        return v.time;
    });

    var svg = d3.select('svg#view');
    var view = svg.select('g.pos-in-seven');

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            var minutes = Math.floor(d.time / 60);
            var seconds = d.time - minutes * 60;
            var tmStr = minutes + '分' + seconds + '秒';
            var valStr = '';

            var redSpanPrefix = '<span style="color:red">';

            if (d.x === 0) {
                valStr = '零徽' + redSpanPrefix + d.y.toFixed(3) + '</span>分';
            } else if (d.x === 14) {
                valStr = '散音';
            } else {
                valStr = redSpanPrefix + BadgeName[d.x] + '</span>徽' + redSpanPrefix + d.y.toFixed(3) + '</span>分';
            }
            return tmStr + '<hr>' + valStr;
        });

    svg.call(tip);

    const viewHeight = +svg.attr('height');
    const viewWidth = +svg.attr('width');

    var xScale = d3.scaleLinear()
        .domain([0, 1])
        .range([viewWidth, 0]);
    var yScale = d3.scaleLinear()
        .domain([0, maxTime])
        .range([0, viewHeight]);

    view.select('g.points')
        .html('')
        .selectAll('circle')
        .data(points.filter(function(v) {
            return v.len > 0 && v.len <= 1;
        }))
        .enter()
        .append('circle')
        .attr('cx', function(v) {
            return xScale(v.len);
        })
        .attr('cy', function(v) {
            return yScale(v.time);
        })
        .attr('r', 2)
        .attr('fill', '#555')
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
}

function loadData(src, cb) {
    d3.text(src, cb);
}

function start() {
    init();
    loadData('./locations.tsv', visualizeChord7);
}

document.ready = start();