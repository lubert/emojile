$(function() {
  function getParam(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  }
  
  // globals
  var $authorize = $('.authorize');
  var $submit = $('.submit');
  var $email = $('.email');
  var $password = $('.password');
  var $team = $('.team');
  var redirect_uri = window.location.protocol + '//' + window.location.host + '/';
  
  // authorization
  var code = getParam('code');
  if (code) {
    $authorize.attr('disabled', true);
    $authorize.text('Authorized!');
  } else {
    $submit.attr('disabled', true);
    $email.attr('disabled', true);
    $password.attr('disabled', true);
    
    $authorize.click(function() {

      window.location = 'https://slack.com/oauth/authorize?client_id=14778368613.14886150994&scope=emoji:read&redirect_uri=' + redirect_uri;
    });
  }

  // submit
  $submit.click(function(e) {
    e.preventDefault();

    var email = $email.val();
    var password = $password.val();
    var team = $team.val();    
    var code = getParam('code');

    if (email && password && code && team) {
      var data = {
        email: email,
        password: password,
        team: team,
        code: code,
        redirect_uri: redirect_uri
      };
      
      $.post('/magic', data, function(res) {
        alert('posted');
      });
    }
  });
});

