function get_data(chef_lis, cur_chef,) {

    // console.log(cur_chef, 'month')
    // console.log(table_num_id, 'menu')
    myajax.post({
        'url': '/cms/chefscoredata/',
        'data': {
            'cur_chef': cur_chef,

        },
        'success': function (data) {
            if (data['code'] === 200) {
                console.log(data['data'])

                function test(data) {

                    var dom = document.getElementById("test");
                    var myChart = echarts.init(dom);
                    var app = {};
                    option = null;
                    setTimeout(function () {

                        option = {
                            legend: [{
                                top: "8%",
                                left: '48%',

                                // icon: "roundRect"
                                data: ['1分', '2分', '3分', '4分', '5分'],
                                icon: "circle",   //  设置形状  类型包括 circle，rect ，roundRect，triangle，diamond，pin，arrow，none
                            },
                                {
                                    top: "8%",
                                    left: '32%',
                                    // icon: "roundRect"
                                    data: ['当月评分量', '当月总分'],
                                    // icon: "circle",   //  设置形状  类型包括 circle，rect ，roundRect，triangle，diamond，pin，arrow，none
                                },
                                {
                                    top: "12%",
                                    // left: '10%',
                                    // icon: "roundRect"
                                    data: data['data']['menu_name'],
                                    icon: "diamond",   //  设置形状  类型包括 circle，rect ，roundRect，triangle，diamond，pin，arrow，none
                                }
                            ],

                            title: {
                                left: 'center',
                                text: '厨师-评分-菜品关系图',
                                top: "2%"
                            },
                            tooltip: {
                                trigger: 'axis',
                                showContent: true,

                            },
                            dataset: [
                                {source: data['data']['month_score_data']},
                                {source: data['data']['month_menu_data']},
                                {source: data['data']['total']}
                            ],
                            xAxis: {type: 'category'},
                            yAxis: [
                                // {gridIndex: 0},
                                {
                                    type: 'value',
                                    name: '当月评分量/份数',
                                    min: 0,
                                    max: data.max,
                                    interval: 10,
                                    // axisLabel: {
                                    //     formatter: '{value} ml'
                                    // }
                                },
                                {
                                    type: 'value',
                                    name: '当月总分',
                                    min: 0,
                                    max: data.max,
                                    interval: 20,
                                    // axisLabel: {
                                    //     formatter: '{value} °C'
                                    // }
                                }
                            ],
                            grid: {top: '55%'},
                            dataZoom: [{
                                type: 'inside',
                                start: 0,
                                end: 100
                            }, {
                                start: 0,
                                end: 10,
                                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                                handleSize: '80%',
                                handleStyle: {
                                    color: '#fff',
                                    shadowBlur: 3,
                                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                                    shadowOffsetX: 2,
                                    shadowOffsetY: 2
                                }
                            }],
                            series: [
                                // {type: 'line', smooth: true, seriesLayoutBy: 'row', datasetIndex: 0},
                                // {type: 'line', smooth: true, seriesLayoutBy: 'row', datasetIndex: 0},
                                // {type: 'line', smooth: true, seriesLayoutBy: 'row', datasetIndex: 0},
                                // {type: 'line', smooth: true, seriesLayoutBy: 'row', datasetIndex: 0},
                                {
                                    type: 'line',
                                    smooth: true,
                                    seriesLayoutBy: 'row',
                                    yAxisIndex: 0,
                                    datasetIndex: 2,
                                    color: ['#0e72cc']
                                },
                                {
                                    type: 'line',
                                    smooth: true,
                                    seriesLayoutBy: 'row',
                                    yAxisIndex: 1,
                                    datasetIndex: 2,
                                    color: ['#f59311']

                                },

                                {
                                    type: 'pie',
                                    id: 'pie',
                                    radius: '25%',
                                    center: ['28%', '35%'],
                                    datasetIndex: 0,
                                    label: {
                                        formatter: '{b}: {@2020-08} ({d}%)'
                                    },
                                    encode: {
                                        itemName: 'date',
                                        value: data['data']['end_date'],
                                        tooltip: data['data']['end_date']
                                    },
                                    // color: ['#63b2ee', '#76da91', '#f8cb7f', '#f89588', '#7cd6cf']
                                    color: ['#50c48f', '#26ccd8', '#3685fe', '#9977ef', '#f47a75'],

                                },

                                {
                                    type: 'pie',
                                    id: 'pie2',
                                    radius: '25%',
                                    center: ['68%', '35%'],
                                    datasetIndex: 1,
                                    label: {
                                        formatter: '{b}: {@2020-08} ({d}%)'
                                    },
                                    encode: {
                                        itemName: 'date',
                                        value: data['data']['end_date'],
                                        tooltip: data['data']['end_date']
                                    },


                                    color: ['#05f8d6', '#0082fc', '#fdd845', '#f47a75', '#22ed7c', '#09b0d3', '#1d27c9', '#f9e264', '#009db2', '#024b51'],


                                }


                            ],
                        };

                        myChart.on('updateAxisPointer', function (event) {
                            var xAxisInfo = event.axesInfo[0];
                            if (xAxisInfo) {
                                var dimension = xAxisInfo.value + 1;
                                myChart.setOption({
                                    series: [{
                                        id: 'pie',
                                        label: {
                                            formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                                        },
                                        encode: {
                                            value: dimension,
                                            tooltip: dimension
                                        }
                                    },
                                        {
                                            id: 'pie2',
                                            label: {
                                                formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                                            },
                                            encode: {
                                                value: dimension,
                                                tooltip: dimension
                                            }
                                        }
                                    ]

                                });
                            }
                        });

                        myChart.setOption(option);

                    });
                    ;
                    if (option && typeof option === "object") {
                        myChart.setOption(option, true);
                    }
                }

                test(data)

            } else {
                myalert.alertInfo('信息有误！')
            }


        }
    })

}

$(function () {

    var chef_lis = document.getElementsByClassName('chef-li')


    for (i = 0; i < chef_lis.length; i++) {
        if (chef_lis[i].classList.contains('active') === true) {
            var cur_chef = chef_lis[i].innerHTML
        }
    }
    get_data(chef_lis, cur_chef)

    for (i = 0; i < chef_lis.length; i++) {
        chef_lis[i].onclick = function () {
            for (i = 0; i < chef_lis.length; i++) {
                if (chef_lis[i].classList.contains('active') === true) {
                    chef_lis[i].classList.remove('active')
                }
            }
            this.classList.add('active')
            var cur_chef = this.innerHTML
            get_data(chef_lis, cur_chef)
        }
    }

})


