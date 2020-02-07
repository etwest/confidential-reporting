openpgp.initWorker({ path:'/static/javascript/openpgp/openpgp.worker.js' }) // set the relative web worker path

// pull data from the 'arguments' to this script
// this is how we establish the recaptcha key and the encryption key
var site_key = document.currentScript.getAttribute('site_key');
var pubkey   = document.currentScript.getAttribute('pubKey');

const Url = '/report'

$( "#form" ).submit(async function( event ) {
  $("#submit").addClass("loading");
  data = $("#name_reported").val();
  // add the optional fields to the email if the user filled it out
  if( $("#reporter").val() != "" ) {
    data += "\n" + $("#reporter").val();
  }
  if( $("#contact").val() != "" ) {
    data += "\n" + $("#contact").val();
  }
  // Add the report text to the end of the email
  data += "\n" + $("#text").val();
  var recaptcha_token = "";
  grecaptcha.ready(function() {
    grecaptcha.execute(site_key,
      {action: 'default'}).then(function(token) {
      recaptcha_token = token;
    })
  })
  $("#encrypt_msg").addClass("shown");
  //Add encryption logic here
  const options = {
      message: openpgp.message.fromText(data),       // input as Message object
      publicKeys: (await openpgp.key.readArmored(pubkey)).keys // for encryption
  }

  openpgp.encrypt(options).then(ciphertext => {
    // '-----BEGIN PGP MESSAGE ... END PGP MESSAGE-----'
    encrypted = ciphertext.data

    // Add timeouts to allow the user to see what is happening
    // Ensures that even if user's computer is fast they still
    // know what's happening
    setTimeout(function() {
      $("#encrypt_msg").removeClass("shown");
      $("#send_msg").addClass("shown");
      $.ajax({
        url: Url,
        type:"PUT",
        data: {report:encrypted, token:recaptcha_token},
        success: function(result){
          $("#submit").addClass("hide-loading");
          $("#send_msg").removeClass("shown")
          $("#done").addClass("shown");
          $("#done_msg").addClass("shown");
        },
        failure: function(result){
          $("#submit").addClass("hide-loading");
          $("#send_msg").removeClass("shown");
          $("#failed").addClass("shown");
          $("#fail_msg").addClass("shown");
          console.log('Error', result);
        },
        error: function(error) {
          $("#submit").addClass("hide-loading");
          $("#send_msg").removeClass("shown");
          $("#failed").addClass("shown");
          $("#fail_msg").addClass("shown");
          console.log('Error', error);
        }
      })
    }, 500);
  })
  event.preventDefault();
});