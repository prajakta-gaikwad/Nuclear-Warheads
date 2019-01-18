function buildPlot() {
    var defaultURL = "/global";
    d3.json(defaultURL).then(function (response) {
        var data = [response];
        console.log(data);

        var layout = {
            showlegend: true,
            title: 'Nuclear Weapons Over Time',
            xaxis: {
                tickfont: {
                    size: 14,
                    color: 'rgb(107, 107, 107)'
                }
            },
            yaxis: {
                title: 'Nuclear Weapons Count',
                titlefont: {
                    size: 16,
                    color: 'rgb(107, 107, 107)'
                },
                tickfont: {
                    size: 14,
                    color: 'rgb(107, 107, 107)'
                }
            },
            legend: {
                x: 0,
                y: 1.0,
            },
            barmode: 'group',
            bargap: 0.15,
            bargroupgap: 0.1
        };

        Plotly.plot("myDiv", data, layout);
    });

}

buildPlot();

function updatePlotly(data) {
    Plotly.restyle("myDiv", "x", [data.x]);
    Plotly.restyle("myDiv", "y", [data.y]);
    Plotly.restyle("myDiv", "name", data.name);
}

function getData(route) {
    d3.json(`/${route}`).then(function (data) {

        //data.forEach({})
        updatePlotly(data);
        });
}

