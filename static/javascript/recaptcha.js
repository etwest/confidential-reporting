var recaptcha_token = "";
var site_key = document.currentScript.getAttribute('site_key');
grecaptcha.ready(function() {
  grecaptcha.execute(site_key,
    {action: 'default'}).then(function(token) {
    recaptcha_token = token;
  })
})