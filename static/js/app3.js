Plotly.d3.csv('../../db/warheads.csv'), function (err, data) {
    // create a lookup table to sort and regroup the columns of data,
    // first by year then by country:
    var lookup = {};
    function getData(year, Entity) {
        var byYear, trace;
        if (!(byYear = lookup[year])) {;
            byYear = lookup[year] = {};
        }
        // if a container for this year + country doesnt exist yet
        // then create one:
        if (!(trace = byYear[Entity])) {
            trace = byYear[Entity] = {
                x: [],
                y: [],
                id: [],
                text: [],
            };
        }
        return trace;
    }

    // Go through each row, get the right trace, and append the data:
    for (var i = 0; i < data.length; i++) {
        var datum = data[i];
        var trace = getData(datum.year, datum.Entity);
        trace.text.push(datum.Entity);
        trace.id.push(datum.Entity);
        trace.x.push(datum.year);
        trace.y.push(datum.count);
    }
    // Get the group names:
    var years = Object.keys(lookup);
    // in this case, every year includes every continent, so we
    // can just infer the continents from the *first* year:
    var firstYear = lookup[years[0]];
    var Entity = Object.keys(firstYear);

    //create the main traces, one for each country:
    var traces = [];
    for (i = 0; i < Entity.length; i++) {
        var data = firstYear[Entity[i]];
        traces.push({
            name: Entity[i],
            x: data.x.slice(),
            y: data.y.slice(),
            id: data.id.slice(),
            text: data.text.slice(),
            mode: 'markers',
        });
    }

    ////
    // Create a frame for each year. Frames are effectively just
    // traces, except they don't need to contain the *full* trace
    // definition (for example, appearance). The frames just need
    // the parts the traces that change (here, the data).
    var frames = [];
    for (i = 0; i < years.length; i++) {
        frames.push({
            name: years[i],
            data: Entity.map(function (Entity) {
                return getData(years[i], Entity);
            })
        })
    }

    // Now create slider steps, one for each frame. The slider
    // executes a plotly.js API command (here, Plotly.animate).
    // In this example, we'll animate to one of the named frames
    // created in the above loop.
    var sliderSteps = [];
    for (i = 0; i < years.length; i++) {
        sliderSteps.push({
            method: 'animate',
            label: years[i],
            args: [[years[i]], {
                mode: 'immediate',
                transition: { duration: 300 },
                frame: { duration: 300, redraw: false },
            }]
        });
    }

    var layout = {
        xaxis: {
            title: 'Year',
            range: [1945, 2014]
        },
        yaxis: {
            title: 'Warhead Count',
            range: [0, 25000]
        },
        hovermode: 'closest',
        // We'll use updatemenus (whose functionality includes menus as
        // well as buttons) to create a play button and a pause button.
        // The play button works by passing `null`, which indicates that
        // Plotly should animate all frames. The pause button works by
        // passing `[null]`, which indicates we'd like to interrupt any
        // currently running animations with a new list of frames. Here
        // The new list of frames is empty, so it halts the animation.
        updatemenus: [{
            x: 0,
            y: 0,
            yanchor: 'top',
            xanchor: 'left',
            showactive: false,
            direction: 'left',
            type: 'buttons',
            pad: { t: 87, r: 10 },
            buttons: [{
                method: 'animate',
                args: [null, {
                    mode: 'immediate',
                    fromcurrent: true,
                    transition: { duration: 300 },
                    frame: { duration: 500, redraw: false }
                }],
                label: 'Play'
            }, {
                method: 'animate',
                args: [[null], {
                    mode: 'immediate',
                    transition: { duration: 0 },
                    frame: { duration: 0, redraw: false }
                }],
                label: 'Pause'
            }]
        }],
        // Finally, add the slider and use `pad` to position it
        // nicely next to the buttons.
        sliders: [{
            pad: { l: 130, t: 55 },
            currentvalue: {
                visible: true,
                prefix: 'Year:',
                xanchor: 'right',
                font: { size: 20, color: '#666' }
            },
            steps: sliderSteps
        }]
    };


    // Create the plot:
    Plotly.newPlot('myDiv', {
        data: traces,
        layout: layout,
        frames: frames,
    });
};