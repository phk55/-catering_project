$(function () {
    $('.del-btn').click(function (event) {
        event.preventDefault();

        var self=$(this)
        var td=self.parent()
        console.log(td)
        var table_num_id=td.attr('data-table-id')
        myajax.post({
            'url':'/cms/deltable/',
            'data':{
                'table_num_id':table_num_id
            },
            'success':function (data) {
                if (data['code']===200){
                    window.location.reload()
                }else{
                    myalert.alertInfo(data['message'])
                }

            }
        })

    })

})