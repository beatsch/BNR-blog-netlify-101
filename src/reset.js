$(document).ready(function() {
  $('#resetdata').click(function(event) {
    event.preventDefault();

    $.ajax({
      type: 'DELETE',
      url: 'http://localhost:8080/phones',
      success: function() {
        location.reload();
      },
    });
  });
});
