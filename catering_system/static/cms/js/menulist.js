$(function () {
    $('.submit-btn').click(function (event) {
        event.preventDefault();
        var formData = new FormData($('#uploadForm')[0]);
        console.log(formData)
        console.log(formData[0])
        $.ajax({
            url: "/cms/addmenulist/",
            type: "POST",
            data: formData,
            async: true,
            cashe: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data['code'] == 200) {
                    myalert.alertSuccessToast('添加成功！');
                    setTimeout(function () {
                        window.location.reload()
                    }, 1000)
                } else {
                    myalert.alertInfo(data['message'])
                }
            },
            error: function (returndata) {
                alert("添加失败！")

            }
        })
    })
})