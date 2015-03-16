function initJournal() {

    var indicator = $('#ajax-progress-indicator');
    var errors = $('#ajax-error-handling');

    $('.day-box input[type="checkbox"]').click(function(event) {
        var box = $(this);

        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'pk': box.data('student-id'),
                'date': box.data('date'),
                'present': box.is(':checked') ? '1': '',
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function(xhr, settings){
                indicator.show()
            },
            'error': function(xhr, status, error) {
                errors.text(error);
                errors.show();
                indicator.hide();
            },
            'success': function(data, status, xhr) {
                indicator.hide();
            }
        });
        
    });
}

$(document).ready(function(){
    initJournal();
});