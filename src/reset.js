$(document).ready(function() {
  $('#resetdata').click(function(event) {
    event.preventDefault();

    $.ajax({
      type: 'DELETE',
      url: 'https://www.vergarntundzugenaeht.de/kindermode',
      success: function() {
        location.reload();
      },
    });
  });
});
