$(function () {
    $('select').selectpicker();
    $('.add-btn-p').click(function (event) {
        event.preventDefault();
        $('#add-modal').modal('show')
    })
    $('.save-btn').click(function (event) {
        event.preventDefault();
        var chef_name = $('input[name="chef_name"]').val()
        var select = document.getElementById('menu_id')
        var menu_id = []
        if (select == null) {
            console.log('ss')
        } else {
            for (var i = 0; i < select.length; i++) {
                if (select.options[i].selected) {
                    menu_id.push(select[i].value)
                }
            }
        }
        if (chef_name === '') {
            myalert.alertInfo('请输入厨师姓名！')
        }

        var menu_id_data = JSON.stringify(menu_id)
        if (menu_id_data === '[]') {
            myalert.alertInfo('请选择烹饪菜品！')
        }

        myajax.post({
            'url': '/cms/chef/',
            'data': {
                'chef_name': chef_name,
                'menu_id_data': menu_id_data
            },
            'success': function (data) {
                console.log('success')
            }
        })


    })
});

$(function () {
    $('.delete-btn').click(function (event) {
        event.preventDefault();
        var self = $(this)

        var chef_name_div = self.parent().parent().parent()
        var chef_name = chef_name_div.attr('data-username')
        console.log(chef_name)
        myalert.alertConfirm({
            'title': '您确定删除该员工吗！',
            'cancelText': '取消',
            'confirmText': '确定',
            'cancelCallback': function () {
                // window.location.reload();
            },
            'confirmCallback': function () {
                myajax.post({
                    'url': '/cms/delchef/',
                    'data': {
                        'chef_name': chef_name
                    },
                    'success': function (data) {
                        if (data['code'] === 200) {
                            window.location.reload();

                        } else {
                            myalert.alertInfo(data['message'])
                        }

                    }
                })

            }
        })

    })
})