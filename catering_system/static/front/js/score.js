$(function () {
    var menu_score_div = document.getElementsByClassName('menu-score-div')
    for (var i = 1; i <= menu_score_div.length; i++) {

        $("#score" + i).lqScore({
            isReScore: true,//允许重新评分
            $tipEle: $("#tip" + i), //提示必须要指定显示的元素，显示样式由你自己定义，如果你不擅长css，可以使用demo中的样式
            tips: ["不推荐", "一般", "不错", "很棒", "极力推荐！"],
            zeroTip: ""
        });
    }


    $("#score0").lqScore({
        isReScore: true,//允许重新评分
        $tipEle: $("#tip0"), //提示必须要指定显示的元素，显示样式由你自己定义，如果你不擅长css，可以使用demo中的样式
        tips: ["不推荐", "一般", "不错", "很棒", "极力推荐！"],
        zeroTip: ""
    });
    // $("#score2").lqScore({
    //     isReScore: true,//允许重新评分
    //     $tipEle: $("#tip2"), //提示必须要指定显示的元素，显示样式由你自己定义，如果你不擅长css，可以使用demo中的样式
    //     tips: ["不推荐", "一般", "不错", "很棒", "极力推荐！"],
    //     zeroTip: ""
    // });
    // $("#score3").lqScore({
    //     isReScore: true,//允许重新评分
    //     $tipEle: $("#tip3"), //提示必须要指定显示的元素，显示样式由你自己定义，如果你不擅长css，可以使用demo中的样式
    //     tips: ["不推荐", "一般", "不错", "很棒", "极力推荐！"],
    //     zeroTip: ""
    // });
    $('.submit-btn').click(function (event) {
        event.preventDefault()
        var menu_score_div = document.getElementsByClassName('menu-score-div')
        var score_array = new Array()
        for (var i = 1; i <= menu_score_div.length; i++) {
            var score = document.getElementById('tip' + i).innerText
            score_array.push(score)

        }

        var score0 = document.getElementById('tip0').innerText
        var suggest = document.getElementById('suggest-text').value
        var ids = document.getElementById('ids').value
        score_array.push(score0, suggest,ids)
        console.log(score_array)
        var score_data = JSON.stringify(score_array)
        // var cur_url = window.location.href
        myajax.post({
            'url': '/addscore/',
            'data': {
                'score_data': score_data

            },
            'success': function (data) {
                if (data['code'] == 200) {
                    window.location.reload()
                } else {
                    myalert.alertInfo(data['message'])
                }

            }
        })


    })
});