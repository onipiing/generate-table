$(document).ready(function () {
    $("#btn-create-html").click(function (e) {
        $.ajax({
            url: '/create_html/',
            method: 'GET',
            // headers: {
            //     'Content-Type': 'application/json',
            // },
            success: function (res) {
                alert('done')
            }
        });
    })
})