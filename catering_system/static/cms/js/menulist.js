$(function () {
    $('.submit-btn').click(function (event) {
        event.preventDefault();
        var formData = new FormData($('#uploadForm')[0]);
        // console.log(formData)
        // console.log(formData[0])
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

    $('.edit-btn').click(function (event) {
        event.preventDefault();
        var add_content = document.getElementById('add-content')
        var edit_btn = document.getElementById('edit-btn')
        var sub_btn = document.getElementById('sub-btn')
        var sold_div = document.getElementById('sold-div')

        if (add_content.classList.contains('hid-css')) {
            add_content.classList.remove('hid-css')
            edit_btn.classList.remove('hid-css')
            sold_div.classList.remove('hid-css')
        } else {
            add_content.classList.add('hid-css')
            edit_btn.classList.add('hid-css')
            sold_div.classList.add('hid-css')
        }
        if (sub_btn.classList.contains('hid-css')) {
            console.log('')
        } else {
            sub_btn.classList.add('hid-css')
        }

        var menuInput = $("input[name='menu_name']")
        var weightInput = $("input[name='weighted_value']")
        var describeInput = $("textarea[name='describe_info']")
        var old_menuInput = $("input[name='old-menu']")

        // console.log(menuInput.val())
        // console.log(weightInput.val())
        // console.log(describeInput.val())
        var self = $(this)

        var menu_id = self.parent().parent().attr('data-menu-id')
        var menu_name_td = document.getElementById('menu-name-' + menu_id)
        var weighted_value_td = document.getElementById('weighted-' + menu_id)
        var desc_td = document.getElementById('desc-' + menu_id)
        var sold_td = document.getElementById('sold-' + menu_id)

        var soldInput = document.getElementById('sold-out')
        var soldLabel = document.getElementById('sold-label')
        if (sold_td.innerHTML === '已下架') {
            soldInput.value = '0'
            soldLabel.innerText = '销售'
        }else {
            soldInput.value = '1'
            soldLabel.innerText = '下架'
        }

        menuInput.val(menu_name_td.innerHTML)
        weightInput.val(weighted_value_td.innerHTML)
        describeInput.val(desc_td.innerHTML)
        old_menuInput.val(menu_name_td.innerHTML)
    })
    $('.edit-submit-btn').click(function (event) {
        event.preventDefault();
        var formData = new FormData($('#uploadForm')[0]);
        // console.log(formData)
        // console.log(formData[0])
        $.ajax({
            url: "/cms/editmenu/",
            type: "POST",
            data: formData,
            async: true,
            cashe: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data['code'] == 200) {
                    myalert.alertSuccessToast('操作成功！');
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

$(function () {
    $('.add-menu').click(function (event) {
        event.preventDefault();
        var add_content = document.getElementById('add-content')
        var sub_btn = document.getElementById('sub-btn')
        var edit_btn = document.getElementById('edit-btn')
        var sold_div = document.getElementById('sold-div')

        if (add_content.classList.contains('hid-css')) {
            add_content.classList.remove('hid-css')
            sub_btn.classList.remove('hid-css')
        } else {
            add_content.classList.add('hid-css')
            sub_btn.classList.add('hid-css')
        }
        if (edit_btn.classList.contains('hid-css')) {
            console.log('')
        } else {
            edit_btn.classList.add('hid-css')

        }
        if (sold_div.classList.contains('hid-css')) {
            console.log('')
        } else {
            edit_btn.classList.add('hid-css')
            sold_div.classList.add('hid-css')
        }

    })
})