function drawChart(pedigree_id, names, links, colors) {

    const ctx = document.getElementById(pedigree_id);
    const label_rotations = [
        0.5*200/2, 1.5*200/2,
        0.5*200/4, 1.5*200/4, 2.5*200/4, 3.5*200/4,
        0.5*200/8, 1.5*200/8, 2.5*200/8, 3.5*200/8, 4.5*200/8, 5.5*200/8, 6.5*200/8, 7.5*200/8,
        0.5*200/16, 1.5*200/16, 2.5*200/16, 3.5*200/16, 4.5*200/16, 5.5*200/16, 6.5*200/16, 7.5*200/16,
            8.5*200/16, 9.5*200/16, 10.5*200/16, 11.5*200/16, 12.5*200/16, 13.5*200/16, 14.5*200/16, 15.5*200/16];
    const label_sizes = [
        16, 16,
        14, 14, 14, 14,
        12, 12, 12, 12, 12, 12, 12, 12,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    ]
    var myChart = new Chart(ctx, {
    plugins: [ChartDataLabels],
    type: 'doughnut',
    data: {
        labels: names,
        datasets: [{
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        backgroundColor: colors
        }, {
        data: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        backgroundColor: colors
        }, {
        data: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        backgroundColor: colors
        }, {
        data: [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        backgroundColor: colors
        }, ]
    },
    options: {
        onClick: (event, elements) =>{
            const clickedElement = elements[0];
            if (clickedElement === undefined) {return;}
            const datasetIndex = clickedElement.index;
            const url = links[datasetIndex];
            if (url != "") {
                window.location.href = url;
            }
        },
        responsive: true,
        maintainAspectRatio: true,
        circumference: 200,
        rotation: -100,
        cutout: "15%",
        hoverBorderColor: "#fff",
        onHover: (event, elements) => {
            const clickedElement = elements[0];
            if (clickedElement === undefined) {return;}
            const datasetIndex = clickedElement.index;
            const url = links[datasetIndex];
            if (url != "") {
                event.native.target.style.cursor = 'pointer';
            } else {
                event.native.target.style.cursor = 'default';
            }
        },
        plugins: {
            datalabels: {
                textAlign: "center",
                anchor: "center",
                formatter: function(value, context) {
                    if (value > 0) {
                        return context.chart.data.labels[context.dataIndex];
                    } else {
                        return null;
                    }
                },
                rotation: function(ctx) {
                  return label_rotations[ctx.dataIndex] - 100;
                },
                font: function(ctx) {
                    if (window.innerWidth > 767) {
                        return {
                            weight: 'normal',
                            size: label_sizes[ctx.dataIndex]
                        };
                    } else {
                        return {
                            weight: 'normal',
                            size: label_sizes[ctx.dataIndex] / 2
                        };
                    }
                }
            },
            tooltip: {mode: false},
            legend: {display: false}}
        }
    });
}
