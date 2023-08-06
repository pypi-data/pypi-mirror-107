var socket = new WebSocket("ws://localhost:" + location.port + "/websocket");

function handle_data(method, msg) {
    console.log(`Handling request: ${method}`);
    if (method == "delete") {
        global_state.clear();
        update_charts(d3.select("#charts"), global_state.chart_list());
        update_series();
    } else if (method == "delete_series") {
        global_state.clear_series();
        update_charts(d3.select("#charts"), global_state.chart_list());
        update_series();
    } else if (method == "delete_charts") {
        global_state.clear_charts();
        update_charts(d3.select("#charts"), global_state.chart_list());
    } else if (method == "read") {
        socket.send(JSON.stringify({
            "method": "save",
            "filename": msg.filename,
            "data": JSON.stringify(global_state)
        }));
    } else if (method == "create_series") {
        if (Array.isArray(msg.data)){
            msg.data.forEach(Series.from_obj);
        }else{
            Series.from_obj(msg.data);
        }
        update_series();
    } else if (method == "create_chart") {
        if (Array.isArray(msg.data)){
            msg.data.forEach(d => global_state.add_chart(Chart.from_obj(d)));
        }else{
            global_state.add_chart(Chart.from_obj(msg.data));
        }
        update_charts(d3.select("#charts"), global_state.chart_list());
    } else if (method == "extend_series") {
        global_state.extend_series(msg.key, msg.data);
    } else if (method == "update") {
        update_charts(d3.select("#charts"), global_state.chart_list());
    } else {
        console.error(`unknown_method:${method}`)
    }
    window.localStorage.setItem("context", JSON.stringify(global_state));
}

socket.onopen = function() {
    console.log("connection established");
};

socket.onclose = function() {
    console.log("connection closed");
};

socket.onerror = function(error) {
    console.log("Error:");
    console.log(error);
};

socket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    let method = data.method;
    delete data.method
    handle_data(method, data);
};

async function save_global_state(fileHandle){
    const writable = await fileHandle.createWritable();
    await writable.write(JSON.stringify(global_state));
    await writable.close();
}

async function load_global_state(fileHandle){
    const file = await fileHandle[0].getFile();
    const text = await file.text();
    global_state = Context.from_obj(JSON.parse(text));
    update_charts();
    update_series();
}


function add_button_methods(){
    d3.select("#nav-data-load").on("click", function(){
        const opts = {
            types: [
                {
                    description: 'JSON File',
                    accept: {
                        'application/json': ['.json']
                    }
                },
            ],
            excludeAcceptAllOption: true,
            multiple: false
        };
        window.showOpenFilePicker(opts)
            .then(load_global_state)
            .catch(console.log);
    });
    d3.select("#nav-data-save").on("click", function(){
        const opts = {
            types: [{
                description: 'JSON File',
                accept: {'application/json': ['.json']},
            }],
        };
        window.showSaveFilePicker(opts)
            .then(save_global_state)
            .catch(console.log);
    });
    d3.select("#nav-data-clear-all").on("click", function(){
        global_state.clear_charts();
        global_state.clear_series();
        update_charts();
        update_series();
    });
    d3.select("#nav-data-clear-series").on("click", function(){
        global_state.clear_series();
        update_charts();
        update_series();
    });
    d3.select("#nav-data-clear-charts").on("click", function(){
        global_state.clear_charts();
        update_charts();
    });
}

window.onload = function() {
    add_button_methods();

    // Try loading data from local storage.
    let context = window.localStorage.getItem("context");
    if (context === null) {
        global_state = new Context();
    } else {
        global_state = Context.from_obj(JSON.parse(context));
    }
    update_charts(d3.select("#charts"), global_state.chart_list());
    update_series(d3.select("#series"), global_state.series_list());
};
