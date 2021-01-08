$(function () {
    myajax.post({
        'url': '/querymenun/',
        'success': function (data) {
            function inputfocus() {
                var demo = document.getElementById('input-div');
                var input = demo.getElementsByTagName('input');
                var menu_detail_div = document.getElementById('menu-detail')
                var iNow = 0;
                type = !-[1,] ? 'onpropertychange' : 'oninput',
                    limit = 3; //满足自动切换焦点的字符数
                for (var i = 0; i < input.length; i++) {
                    input[i].index = i;
                    input[i][type] = function () {
                        iNow = this.index;
                        var that = this;
                        // console.log(input.length)
                        // console.log(iNow)
                        input = demo.getElementsByTagName('input');
                        if (iNow === input.length - 1) {
                            var menuinputdiv = document.getElementById('menu-input-div');
                            var inputDemo = document.createElement('input')
                            inputDemo.classList.add('menu-num')
                            inputDemo.maxLength = 3
                            var span = document.createElement('span')
                            span.innerText = '-'
                            menuinputdiv.appendChild(span)
                            menuinputdiv.appendChild(inputDemo)
                            inputfocus()
                        }
                        setTimeout(function () {
                            var cur_menu = new Array()
                            var cur_num = new Array()
                            for (var i = 0; i < input.length - 1; i++)
                                if (i === 0) {
                                    if (typeof (data['data']['table_dict'][input[i].value]) == "undefined") {
                                        input[i].classList.add('error')
                                    } else {
                                        input[i].classList.remove('error')
                                    }
                                } else {
                                    if (typeof (data['data']['menu_dict'][input[i].value]) == "undefined" && input[i].value) {
                                        input[i].classList.add('error')
                                    } else {
                                        input[i].classList.remove('error')
                                        cur_menu.push(data['data']['menu_dict'][input[i].value])
                                        cur_num.push(input[i].value)
                                    }
                                }
                            console.log(cur_num.length)
                            console.log(cur_menu)
                            // console.log(input[iNow - 1])
                            // console.log(data['data'][input[iNow - 1].value], 'dd')
                            var menu_tem = document.getElementById('menu-tem')
                            menu_tem.remove()
                            var menu_tem_new = document.createElement('ul')
                            menu_tem_new.id = 'menu-tem'
                            for (var j = 0; j < cur_menu.length; j++) {
                                var li = document.createElement('li')
                                li.innerText = cur_num[j] + '. ' + cur_menu[j]
                                menu_tem_new.appendChild(li)
                            }
                            menu_detail_div.appendChild(menu_tem_new)


                            that.value.length > limit - 1 && input[iNow + 1].focus();
                            if (iNow === 0) {
                                $('input:text:first').focus();
                                var $inp = $('input:text');
                                $inp.bind('keydown', function (e) {
                                    var key = e.which;
                                    if (key == 13) {
                                        e.preventDefault();
                                        var nxtIdx = $inp.index(this) + 1;
                                        $(":input:text:eq(" + nxtIdx + ")").focus();
                                    }
                                });
                            }
                        }, 0)
                    }
                }
            }

            inputfocus()
            // console.log(data)
        }
    })


})


$(function () {
    $('#print-btn').click(function (event) {
        event.preventDefault()
        var inputs = document.getElementsByClassName('menu-num')
        var num_array = new Array()
        for (var i = 0; i < inputs.length; i++) {
            var text = inputs[i].value
            if (text) {
                num_array.push(text)
            }


        }

        var num_data = JSON.stringify(num_array)
        console.log(num_data)
        myajax.post({
            'url': '/placeorder/',
            'data': {
                'num_data': num_data
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    myalert.alertSuccessToast('success!')
                    // setTimeout(function () {
                    //     window.location.reload()
                    // }, 8000)
                } else {
                    myalert.alertInfo(data['message'])
                }

            }


        })


    })

})