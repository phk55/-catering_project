$(function () {
    $("#score1").lqScore({
        isReScore: true,//允许重新评分
        $tipEle: $("#tip1"), //提示必须要指定显示的元素，显示样式由你自己定义，如果你不擅长css，可以使用demo中的样式
        tips: ["不推荐", "一般", "不错", "很棒", "极力推荐！"],
        zeroTip: ""
    });
    $("#score2").lqScore({
        isReScore: true,//允许重新评分
        $tipEle: $("#tip2"), //提示必须要指定显示的元素，显示样式由你自己定义，如果你不擅长css，可以使用demo中的样式
        tips: ["不推荐", "一般", "不错", "很棒", "极力推荐！"],
        zeroTip: ""
    });
    $("#score3").lqScore({
        isReScore: true,//允许重新评分
        $tipEle: $("#tip3"), //提示必须要指定显示的元素，显示样式由你自己定义，如果你不擅长css，可以使用demo中的样式
        tips: ["不推荐", "一般", "不错", "很棒", "极力推荐！"],
        zeroTip: ""
    });
    $('.submit-btn').click(function (event) {
        event.preventDefault()
        var score1=document.getElementById('tip1').innerText
        var score2=document.getElementById('tip2').innerText
        var score3=document.getElementById('tip3').innerText
        var suggest=document.getElementById('suggest-text').value

        var cur_url=window.location.href
        myajax.post({
            'url':'/addscore/',
            'data':{
                'score1':score1,
                'score2':score2,
                'score3':score3,
                'suggest':suggest,
                'cur_url':cur_url
            },
            'success':function (data) {
                if (data['code']==200){
                    window.location.reload()
                }else {
                    myalert.alertInfo(data['message'])
                }

            }
        })


    })
});