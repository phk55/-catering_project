$(function () {
    $("#aui-btn-reg").click(function (event) {
        event.preventDefault()
        if (!verifyCheck._click()) return;
        var phone = $("input[name='phone']").val()
        var pwd = $("input[id='password']").val()
        console.log('sss')
        myajax.post({
            'url': '/cms/login/',
            'data': {
                'phone': phone,
                'pwd': pwd,
                'verify': 1

            },
            'success': function (data) {
                if (data['code'] === 200) {
                    window.location = '/cms/'
                } else {
                    myalert.alertInfo(data['message'])
                }

            }
        })

    });
    $("#aui-btn-reg1").click(function () {
        if (!verifyCheck._click()) return;
        var phone = $("input[name='phone-verify']").val()
        var verify = $("input[id='verifyNo']").val()

        myajax.post({
            'url': '/cms/login/',
            'data': {
                'phone': phone,
                'pwd': 1,
                'verify': verify

            },
            'success': function (data) {
                if (data['code'] === 200) {
                    window.location = '/cms/'
                } else {
                    myalert.alertInfo(data['message'])
                }

            }
        })

    });
});