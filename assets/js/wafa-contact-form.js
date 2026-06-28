(function () {
  var form = document.getElementById('wafa-contact-form');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = (form.querySelector('[name="name"]') || {}).value || '';
    var email = (form.querySelector('[name="email"]') || {}).value || '';
    var subject = (form.querySelector('[name="subject"]') || {}).value || 'Website enquiry';
    var message = (form.querySelector('[name="message"]') || {}).value || '';

    var body =
      'Name: ' + name + '\n' +
      'Email: ' + email + '\n\n' +
      message;

    var href =
      'mailto:info@wafaenterprises.com' +
      '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(body);

    window.location.href = href;
  });
})();
