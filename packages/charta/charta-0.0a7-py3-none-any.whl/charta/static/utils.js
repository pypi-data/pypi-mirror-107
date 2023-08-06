function rect_from_pts(x, y, x2, y2) {
    let width = x2 - x;
    let height = y2 - y;
    if (width < 0) {
        width = -width;
        x = x - width;
    }
    if (height < 0) {
        height = -height;
        y = y - height;
    }

    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
    };
}

function collapse_extents(extents) {
    return [d3.min(extents, d => d[0]), d3.max(extents, d => d[1])];
}

function zoom_center(bounds, mag, pos) {
    return bounds.map(b => (b - pos) / mag + pos);
}

function pad_extent(extent, frac) {
    half_extent = frac * (extent[1] - extent[0]) / 2;
    mean = (extent[1] + extent[0]) / 2;
    return [mean - half_extent, mean + half_extent];
}

function svg_coords(svg, point, use_screen = false) {
    let pt = svg.createSVGPoint();
    pt.x = point.x;
    pt.y = point.y;
    let svg_pt = undefined;
    if (use_screen) {
        svg_pt = pt.matrixTransform(svg.getScreenCTM().inverse());
    } else {
        svg_pt = pt.matrixTransform(svg.getCTM().inverse());
    }
    return {
        "x": svg_pt.x,
        "y": svg_pt.y
    };

}
