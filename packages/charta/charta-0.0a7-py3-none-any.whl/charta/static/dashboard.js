function update_charts(charts_container, data) {
    if (arguments.length < 1){
        charts_container = d3.select("#charts");
    }
    if (arguments.length < 2){
        data = global_state.chart_list();
    }

    if (data.length > 0) {
        charts_container.select(".no_charts").style("display", "none");
    } else {
        charts_container.select(".no_charts").style("display", null);
    }

    let charts = charts_container
        .selectAll("div.chart")
        .data(data, d => d.key);

    let new_charts = charts.enter()
        .append("div").classed("chart", true);

    let svg = new_charts.append("svg").attr("viewBox", chart => [0, 0, chart.visual.width, chart.visual.height])
    svg.append("defs").append("clipPath").attr("id", chart => `${chart.key}-graph-window`).append("rect");
    let g_container = svg.append("g").attr("pointer-events", "bounding-box");
    g_container.append("g").classed("xaxis", true);
    g_container.append("g").classed("yaxis", true);
    g_container.append("g").classed("series", true)
        .attr("clip-path", chart => `url(#${chart.key}-graph-window)`)
        .append("rect")
        .classed("zoom_box", true)
        .attr("fill", "steelblue")
        .attr("opacity", 0.0);

    new_charts.merge(charts)
        .attr("id", d => d.key)
        .each(d => update_chart(d));

    charts.exit().remove();
}

function line_key(chart_key, x_key, y_key) {
    return `${chart_key}-${x_key}-${y_key}`;
}

function update_chart(chart) {
    let x_scale = chart.x_scale();
    let y_scale = chart.y_scale();
    let chart_div = d3.select("#" + chart.key);

    filter_fn = function (series){
        return (series[0] in global_state.series) && (series[1] in global_state.series);
    }

    chart.series = chart.series.filter(filter_fn);

    // Define clipping window
    chart_div.select(`#${chart.key}-graph-window`)
        .select("rect")
        .attr("x", chart.visual.margin)
        .attr("y", chart.visual.margin)
        .attr("width", chart.visual.width - 2 * chart.visual.margin)
        .attr("height", chart.visual.height - 2 * chart.visual.margin)

    // Draw axes.
    x_scale.clamp(true);
    y_scale.clamp(true);
    chart_div.select("g.xaxis")
        .call(d3.axisBottom(x_scale))
        .attr("transform", `translate(0,${y_scale(0)})`);
    chart_div.select("g.yaxis")
        .call(d3.axisLeft(y_scale))
        .attr("transform", `translate(${x_scale(0)},0)`);
    x_scale.clamp(false);
    y_scale.clamp(false);

    // Bind interactions.
    chart_div.on("dblclick", function(event) {
        chart.reset_zoom();
        update_chart(chart);
    });

    make_drag_zoomable(chart_div, chart, update_chart);
    make_wheel_zoomable(chart_div, chart, update_chart);

    // Draw lines.
    let lines = chart_div.select(".series")
        .selectAll("g.line")
        .data(chart.series.map(keys => [global_state.series[keys[0]], global_state.series[keys[1]]]));

    let new_lines = lines.enter()
        .append("g")
        .classed("line", true)
        .attr("id", d => line_key(chart.key, d[0].key, d[1].key));
    new_lines.append("path");

    new_lines.merge(lines)
        .each(d => update_line(chart, d[0], d[1], x_scale, y_scale));

    lines.exit()
        .remove();
}

function update_line(chart, x_series, y_series, x_scale, y_scale) {
    let key = line_key(chart.key, x_series.key, y_series.key);
    let data = x_series.data.map((x, i) => [x_scale(x), y_scale(y_series.data[i])]);

    g_series =
        d3.select("g#" + key);

    // Add the line.
    g_series.select("path")
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("d", d3.line()(data));

    // Add the circles
    let circles = g_series.selectAll("circle")
        .data(data);
    circles.enter()
        .append("circle")
        .attr("fill", "white")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .merge(circles)
        .attr("cx", d => d[0])
        .attr("cy", d => d[1])
        .attr("r", 2);
}

var global_state = {
    "series": {},
    "charts": {},
    "active_charts": []
};

function update_series(selection, series) {
    if (arguments.length < 1) {
        selection = d3.select("#series");
    }
    if (arguments.length < 2) {
        series = global_state.series_list();
    }
    divs = selection.selectAll("div")
        .data(series);

    let new_divs = divs.enter()
        .append("div")
        .classed("series-item", true);

    new_divs.append("p");

    new_divs.merge(divs)
        .attr("title", d => d.key)
        .select("p")
        .text(d => d.key);

    divs.exit().remove();
    return selection;
}

class Context {
    static from_obj(obj) {
        let ctx = new Context();
        for (const key in obj.series) {
            ctx.series[key] = Series.from_obj(obj["series"][key]);
        }
        for (const key in obj.charts) {
            ctx.charts[key] = Chart.from_obj(obj["charts"][key]);
        }
        return ctx;
    }

    constructor() {
        this.series = {};
        this.charts = {};
    }

    chart_list() {
        return Object.keys(this.charts).map(k => this.charts[k]);
    }

    series_list() {
        return Object.keys(this.series).map(k => this.series[k]);
    }

    add_chart(chart) {
        if (this.charts.hasOwnProperty(chart.key)) {
            console.error(`key_error:chart with the key ${chart.key} already exists, renaming to ${chart.key}_new`);
            chart.key = chart.key + "_new";
            this.add_chart(chart);
        }
        this.charts[chart.key] = chart;
    }

    extend_series(key, data) {
        this.series[key].extend(data);
    }

    clear_series() {
        this.series = {};
        for (const chart_key in this.charts) {
            this.charts[chart_key].series = this.charts[chart_key].series.filter(s => s[0] in this.series && s[1] in this.series);
        }
    }

    clear_charts() {
        this.charts = {};
    }

    clear() {
        this.clear_charts();
        this.clear_series();
    }
}

var global_state = new Context();

class Series {
    static from_obj(obj) {
        return new Series(obj.key, obj.data)
    }

    constructor(key, data) {
        this.key = key;
        this.data = data;
        global_state.series[key] = this;
    }

    extent() {
        if (this.data.length == 0) {
            return [-1, 1];
        }
        return d3.extent(this.data);
    }

    extend(data) {
        this.data = this.data.concat(data);
        return this;
    }

    append(data) {
        this.data.push(data);
        return this;
    }
}

class ChartVisual {
    constructor() {
        this.height = 300;
        this.width = 1000;
        this.margin = 40;
        this.x_bounds = undefined;
        this.y_bounds = undefined;
        this.zoom_box_x = undefined;
        this.zoom_box_y = undefined;
    }
}

class Chart {
    static from_obj(obj) {
        return new Chart(obj["key"], obj["series"]);
    }

    constructor(key, series) {
        this.key = key;
        this.series = series;
        this.visual = new ChartVisual();
    }

    x_scale() {
        return d3.scaleLinear()
            .domain(this.x_extent_visual(1.05)) // Make the max zoom 5% larger than the data range.
            .range([this.visual.margin, this.visual.width - this.visual.margin]);
    }

    y_scale() {
        return d3.scaleLinear()
            .domain(this.y_extent_visual(1.05)) // Make the max zoom 5% larger than the data range.
            .range([this.visual.height - this.visual.margin, this.visual.margin]);
    }

    x_extent() {
        if (this.series.length == 0) {
            return [-1, 1];
        }
        return collapse_extents(this.series.map(d => global_state.series[d[0]].extent()))
    }

    y_extent() {
        if (this.series.length == 0) {
            return [-1, 1];
        }
        return collapse_extents(this.series.map(d => global_state.series[d[1]].extent()))
    }

    reset_zoom() {
        this.visual.x_bounds = undefined;
        this.visual.y_bounds = undefined;
    }

    zoom_x(mag, pos) {
        this.visual.x_bounds = zoom_center(this.x_extent_visual(), mag, pos)
    }

    zoom_y(mag, pos) {
        this.visual.y_bounds = zoom_center(this.y_extent_visual(), mag, pos)
    }

    x_extent_visual(padding) {
        if (this.visual.x_bounds === undefined) {
            if (padding) {
                return pad_extent(this.x_extent(), padding);
            }
            return this.x_extent();
        }
        let extent = this.x_extent();
        extent = [Math.max(extent[0], this.visual.x_bounds[0]), Math.min(extent[1], this.visual.x_bounds[1])];
        if (padding) {
            return pad_extent(extent, padding);
        }
        return extent;
    }

    y_extent_visual(padding) {
        if (this.visual.y_bounds === undefined) {
            if (padding) {
                return pad_extent(this.y_extent(), padding);
            }
            return this.y_extent();
        }
        let extent = this.y_extent();
        extent = [Math.max(extent[0], this.visual.y_bounds[0]), Math.min(extent[1], this.visual.y_bounds[1])];
        if (padding) {
            return pad_extent(extent, padding);
        }
        return extent;
    }
}
