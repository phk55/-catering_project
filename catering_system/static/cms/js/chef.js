$(function () {
    $('select').selectpicker();
    $('.add-btn-p').click(function (event){
        event.preventDefault();
        $('#add-modal').modal('show')
    })
});