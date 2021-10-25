$('.sheet-changer-btn').click( function() {
    $('.sheet-changer-btn').removeClass('active');
    $(this).addClass('active');
    $('.sheet_table').css('display', 'None');
    const id = $(this).find("input").attr('value');
    $('#sheet_table-'+id).css('display', 'block');
} );

$(document).ready( function () {
    $('table.dataTable').DataTable({
        "scrollX": true
    });
    $('#sheet-changer-1').click()
} );