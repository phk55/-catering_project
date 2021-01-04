$(function () {
    $('select').selectpicker();
    $('.add-btn-p').click(function (event) {
        event.preventDefault();
        $('#add-modal').modal('show')
    })
    $('.save-btn').click(function (event) {
        event.preventDefault();
        var chef_name = $('input[name="chef_name"]').val()
        var tag_input = document.getElementById('tag-input').innerText


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
                'menu_id_data': menu_id_data,
                'tag': tag_input
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    myalert.alertSuccessToast()
                    setTimeout(function () {
                        window.location.reload()
                    }, 500)
                } else {
                    myalert.alertInfo(data['message'])
                }
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
    $('.edit-btn').click(function (event) {
        event.preventDefault();
        var self = $(this)
        var chef_name_div = self.parent().parent().parent()
        var chef_name = chef_name_div.attr('data-username')
        var menu_li = document.getElementById(chef_name).getElementsByTagName('li')
        var select = document.getElementById('menu_id')
        // for (var i = 0; i < select.options.length; i++) {
        //     if (select.options[i].value in menu_array) {
        //         select.options[i].selected = true;
        //     }
        // }

        // console.log(menu_li)

        var menu_array = new Array()
        for (var i = 0; i < menu_li.length; i++) {
            // console.log(menu_li[i].value)
            menu_array.push(menu_li[i].value)
        }
        console.log(menu_array, '66')
        $('#add-modal').modal('show')
        var chef_name_input = $("input[id='chef-name-input']")
        var tag_input = document.getElementById('tag-input')

        tag_input.innerText = 1
        chef_name_input.val(chef_name)

        for (var j = 0; j < select.options.length; j++) {


            select.options[j].selected = menu_array.indexOf(parseInt(select.options[j].value)) !== -1;
            // select.options[j].selected = select.options[j].value in menu_array;
        }

        $('#menu_id').selectpicker('refresh')

        console.log(tag_input.innerText, 'hdjsdhjs')
    })
})