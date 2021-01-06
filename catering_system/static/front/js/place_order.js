$(function () {
    var demo = document.getElementById('demo');
    input = demo.getElementsByTagName('input');
    var iNow = 0;
    type = !-[1,] ? 'onpropertychange' : 'oninput',
        limit = 3; //满足自动切换焦点的字符数
    for (var i = 0; i < input.length - 1; i++) {
        input[i].index = i;

        input[i][type] = function () {
            iNow = this.index;
            var that = this;
            setTimeout(function () {
                that.value.length > limit - 1 && input[iNow + 1].focus();
                console.log(input[i])
            }, 0)
        }
    }

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
        var num_data=JSON.stringify(num_array)
        console.log(num_data)
        myajax.post({
            'url':'/placeorder/',
            'data':{
                'num_data':num_data
            },
            'success':function (data) {
                if (data['code']===200){
                    myalert.alertSuccessToast('success!')
                    setTimeout(function () {
                        window.location.reload()
                    },800)
                }else {
                    myalert.alertInfo(data['message'])
                }

            }


        })

    })

})