"use strict";

$.get('/adjective', (response) => {
  $('#adjective').text(response);
});

"use strict";

$('#delivery-form').on('submit', (evt) => {
  evt.preventDefault();

  // Get user input from a form
  const formData = {
    city: $('#city-field').val(),
    address: $('#adr-field').val()
  };

  // Send formData to the server (becomes a query string)
  $.get('/delivery-info.json', formData, (res) => {
    // Display response from the server
    alert(`This will cost $${res.cost}`);
    alert(`This will arrive in ${res.days} day(s)`);
  });
});

"use strict";

$('#update-status').on('click', () => {
  // Our GET request URL will look like this:
  //       /status?order=123
  $.get('/status', { order: 123 }, (res) => {
    $('#order-status').html(res);
  });
});

"use strict";

$('#order-form').on('submit', (evt) => {
  evt.preventDefault();

  const formInputs = {
    'type': $('#type-field').val(),
    'amount': $('#amount-field').val()
  };

  $.post('/new-order', formInputs, (res) => {
    alert(res);
  });
});
