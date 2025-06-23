/*
Template Name: Reback - Responsive 5 Admin Dashboard
Author: Techzaa
File: profile js
*/


class Profile {

    init() {
        this.initEarning();
    }

    initEarning() {

        const chartElement = document.getElementById("earning");

        const options = {
            colors: ['#e8ebee', '#5B8DEC'], chart: {
                height: 289, type: 'bar', endingShape: 'rounded', toolbar: {
                    show: false
                }
            }, plotOptions: {
                bar: {
                    horizontal: false, endingShape: 'rounded', columnWidth: '45%',
                },
            }, dataLabels: {
                enabled: false
            }, stroke: {
                show: true, width: 2, colors: ['transparent']
            }, series: [{
                name: 'Client', data: [250, 600, 355, 450, 485, 598, 760, 760, 450, 860, 600, 350]
            }, {
                name: 'Design', data: [450, 750, 550, 700, 615, 735, 1000, 895, 650, 990, 760, 500]
            }], xaxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            }, fill: {
                type: 'solid', opacity: .8
            }, legend: {
                offsetY: 7,
            }, yaxis: {
                title: {
                    text: ''
                }
            }, grid: {
                row: {
                    colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.2
                }, borderColor: '#f1f3fa'
            }, tooltip: {
                y: {
                    formatter: function (val) {
                        return val
                    }
                }
            }
        };

        const chart = new ApexCharts(chartElement, options);

        chart.render();
    }
}

document.addEventListener('DOMContentLoaded', function (e) {
    new Profile().init();
});