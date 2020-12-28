function get_data(month_lis, menu_lis, cur_month, cur_menu_id) {
    if (cur_menu_id === 0) {
        for (i = 0; i < menu_lis.length; i++) {
            if (menu_lis[i].classList.contains('active') === true) {
                cur_menu_id = menu_lis[i].value

            }
        }
    }
    if (cur_month === 0) {
        for (i = 0; i < month_lis.length; i++) {
            if (month_lis[i].classList.contains('active') === true) {
                cur_month = month_lis[i].innerHTML
            }
        }
    }
    console.log(cur_month, 'month')
    console.log(cur_menu_id, 'menu')
    myajax.post({
        'url': '/cms/scoredata/',
        'data': {
            'cur_month': cur_month,
            'cur_menu_id': cur_menu_id
        },
        'success': function (data) {
            if (data['code'] === 200) {

            } else {
                myalert.alertInfo('信息有误！')
            }


        }
    })

}

$(function () {
    var month_lis = document.getElementsByClassName('month-li')
    var menu_lis = document.getElementsByClassName('menu-li')
    for (i = 0; i < month_lis.length; i++) {
        month_lis[i].onclick = function () {
            for (i = 0; i < month_lis.length; i++) {
                if (month_lis[i].classList.contains('active') === true) {
                    month_lis[i].classList.remove('active')
                }
            }
            this.classList.add('active')
            var cur_month = this.innerHTML
            get_data(month_lis, menu_lis, cur_month, 0)
        }
    }

    for (i = 0; i < menu_lis.length; i++) {
        menu_lis[i].onclick = function () {
            for (i = 0; i < menu_lis.length; i++) {
                if (menu_lis[i].classList.contains('active') === true) {
                    menu_lis[i].classList.remove('active')

                }
            }
            this.classList.add('active')
            var cur_menu_id = this.value
            get_data(month_lis, menu_lis, 0, cur_menu_id)
        }
    }
    console.log('dhfgdsfhdghf')

})