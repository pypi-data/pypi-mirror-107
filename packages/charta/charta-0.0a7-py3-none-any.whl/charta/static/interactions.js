function make_wheel_zoomable(chart_div, chart, update) {
	let x_scale = chart.x_scale();
	let y_scale = chart.y_scale();

	chart_div.select("svg g").on("wheel", function(e) {
		let pt = svg_coords(chart_div.select("svg").node(), e, true);
		if (e.ctrlKey) {
			chart.zoom_y(Math.exp(e.deltaY / 300.0), y_scale.invert(pt.y));
		} else {
			chart.zoom_x(Math.exp(e.deltaY / 300.0), x_scale.invert(pt.x));
		}
		update(chart);
		e.preventDefault();
	});
}


function make_drag_zoomable(chart_div, chart, update) {

	let drag = d3.drag().filter(true)
		.on("start", function(e) {
			e.sourceEvent.ctrlKey ? console.log(e) : zoom_start_drag(e, chart_div, chart);
		})
		.on("drag", function(e) {
			e.sourceEvent.ctrlKey ? console.log(e) : zoom_dragging(e, chart_div, chart);
		})
		.on("end", function(e) {
			e.sourceEvent.ctrlKey ? {} : zoom_end_drag(e, chart_div, chart, update);
		});

	chart_div.select("svg g").call(drag);
}

function zoom_start_drag(e, chart_div, chart) {
	chart.visual.zoom_box_x = e.x;
	chart.visual.zoom_box_y = e.y;
	chart_div.select(".zoom_box")
		.attr("opacity", 0.2)
		.attr("x", e.x)
		.attr("y", e.y)
		.attr("width", 0)
		.attr("height", 0);
}


function zoom_dragging(e, chart_div, chart) {
	let rect = rect_from_pts(chart.visual.zoom_box_x, chart.visual.zoom_box_y, e.x, e.y);
	chart_div.select(".zoom_box")
		.attr("width", rect.width)
		.attr("height", rect.height)
		.attr("x", rect.x)
		.attr("y", rect.y);
}

function zoom_end_drag(e, chart_div, chart, update) {
	if (e.x == chart.visual.zoom_box_x || e.y == chart.visual.zoom_box_y) {
		return;
	}
	let x_min = Math.min(e.x, chart.visual.zoom_box_x);
	let x_max = Math.max(e.x, chart.visual.zoom_box_x);
	let y_min = Math.min(e.y, chart.visual.zoom_box_y);
	let y_max = Math.max(e.y, chart.visual.zoom_box_y);

	let x_scale = chart.x_scale();
	let y_scale = chart.y_scale();

	chart.visual.x_bounds = [x_scale.invert(x_min), x_scale.invert(x_max)]
	chart.visual.y_bounds = [y_scale.invert(y_max), y_scale.invert(y_min)]

	chart_div.select(".zoom_box").attr("opacity", 0.0);
	update(chart);
}
