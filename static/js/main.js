var API_URL_SET = 'http://' + location.host + '/api/set',
    $modal = $('#modal').modal({show: false});



$(document).ready(function () {

    $(function () {
        $('#set').click(function () {
            $modal.modal('show');
        });


        $modal.find('.submit').click(function () {

            $.ajax({
                url: API_URL_SET,
                type: 'post',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({"key": $('#modal_key').val(), "value": $('#modal_value').val()}),

                success: function () {
                    // clear from
                    $('#modal_key').val('');
                    $('#value_key').val('');
                    $modal.modal('hide');

                    //reload page
                    location.reload();

                },
                error: function () {
                    $modal.modal('hide');
                }
            });
        });


    })


});

// function return back
function goBack() {
    window.history.back();
}