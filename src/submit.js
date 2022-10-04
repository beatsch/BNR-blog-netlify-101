$(document).ready(function() {
  $('#form').submit(function(event) {
    event.preventDefault();

    var brand = $('#brand').val();
    var model = $('#model').val();
    var os = $('#os').val();
    var screensize = $('#screensize').val();
    var image = $('#inputimageurl').val();

    $.ajax({
      type: 'POST',
      url: 'https://www.vergarntundzugenaeht.de/kindermode',
      data: {brand: brand, model: model, os: os, screensize: screensize, image: image},
      contentType: 'application/json',
      // dataType: "json",
      success: function() {
        location.reload();
      },
    });
  });
});
