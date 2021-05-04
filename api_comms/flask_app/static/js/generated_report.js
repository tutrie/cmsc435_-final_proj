

$('.btn').click( function() {
    $('.btn').removeClass('active');
    $(this).addClass('active');
    $('.sheet_table').css('display', 'None');
    const id = $(this).find("input").attr('value');
    $('#sheet_table-'+id).css('display', 'block');
} );

$(document).ready( function () {
    $('table.dataTable').DataTable();
    $('#btn-1').click()
} );