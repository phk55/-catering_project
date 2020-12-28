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

                var score_data = data['data']['score_data']
                var chef_data = data['data']['chef_name']

                // console.log(data['data'])
                // console.log(Object.keys(score_data))
                var table = document.getElementById('score_table')
                var old_tb = document.getElementById('tb')
                old_tb.remove()
                var tb=document.createElement('tbody')
                tb.id='tb'
                table.appendChild(tb)

                var score_data_keys = Object.keys(score_data)
                for (var i = 0; i < score_data_keys.length; i++) {
                    var tr = document.createElement('tr')
                    var td1 = document.createElement('td')
                    td1.innerText = i + 1
                    var td2 = document.createElement('td')
                    td2.innerText = score_data[i]['score1']
                    var td3 = document.createElement('td')
                    td3.innerText = score_data[i]['score2']
                    var td4 = document.createElement('td')
                    td4.innerText = score_data[i]['score3']
                    var td5 = document.createElement('td')
                    td5.innerText = score_data[i]['suggest']

                    var td6 = document.createElement('td')
                    td6.innerText = score_data[i]['create_time']
                    tr.appendChild(td1)
                    tr.appendChild(td2)
                    tr.appendChild(td3)
                    tr.appendChild(td4)
                    tr.appendChild(td5)
                    tr.appendChild(td6)
                    tb.appendChild(tr)
                }


                var chef_div=document.getElementById('chef_div')
                var old_user_div=document.getElementById('user_div')
                old_user_div.remove()
                var user_div=document.createElement('div')
                user_div.id='user_div'
                chef_div.appendChild(user_div)

                for (var j=0;j<chef_data.length;j++){
                    var span=document.createElement('span')
                    span.innerText=chef_data[j]
                    user_div.appendChild(span)
                }


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