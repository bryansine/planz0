$(document).ready(function() {
    $('#eventDetailsBookBtn').click(function() {
      $('.ui.modal').modal('show');
    });

    $('#eventDetailForm').submit(function(e) {
      e.preventDefault(); 
      var formData = $(this).serialize();

      $.ajax({
        type: 'POST',
        url : "{% url 'home:eventDetail' event.id %}",
        data: formData,
        success: function(response) {
          console.log('Form submitted successfully', response);
          $('#eventDetailsMessage').show();
          setTimeout(function() { $('#eventDetailsMessage').fadeOut('slow'); }, 5000);
        },
        error: function(error) {
          console.error('Error submitting form', error);
        }
      });

      $('.ui.modal').modal('hide');
    });
});

$(document).ready(function() {
    $('#homeCreateBtn').click(function() {
      $('.ui.modal').modal('show');
    });
});

// --------- Might have to check this if else block again
// Check if the session variable indicates a successful event creation
var eventCreated = false;
if (request.session.eventCreated)
    var eventCreated = true

if (eventCreated) {
    $('#homeEventMessage').show();
    setTimeout(function() {
    $('#homeEventMessage').fadeOut('slow');
    }, 5000);  // Hide after 5 seconds
}

$('.item').click(function() {
$('.item').eq(1).click();
});
