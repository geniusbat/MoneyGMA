var config = {}
window.onload = function() {
    return;
    console.log(document.getElementById("data"))
    config = {
        type: 'pie',
        data: {
        datasets: [{
            data: document.getElementById("data").value,
            backgroundColor: [
            '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
            ],
            label: 'Population'
        }],
        labels: document.getElementById("labels").value
        },
        options: {
        responsive: true
        }
    };
    var ctx = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctx, config);
    console.log("FF")
};