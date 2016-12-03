$(document).ready(function () {
    var frm = $('#discount'),
        total = $('#total-sum');

    frm.submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                var error = data.error;
                if (error){
                    alert(error)
                } else {
                   alert(data.success);
                    total.html(data.total);
                }

            }
        });
        return false;
    });
});
