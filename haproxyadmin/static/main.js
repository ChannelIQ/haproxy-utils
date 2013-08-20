$(document).ready(function() {
    $('input.selectAll').change(function() {
        var checkState = $(this).is(":checked");
        $('input.server_row').each(function() {
            if($(this).parent().parent().is(":visible")) {
                $(this).prop('checked', checkState);
            }
        });
    });
});
