document.addEventListener('DOMContentLoaded', () => {
  $("#contactForm").submit(function( event ) {
    const xhr = new XMLHttpRequest();
    var csrf_token = document.getElementById('csrf_token').value;
    var form_data = new FormData();
    url = '/contact';

    button = document.getElementById('submitContact');
    button.value = "Sending...";

    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var subject = document.getElementById('subject').value;
    var message = document.getElementById('message').value;
    var honey = document.getElementById('honey').value;

    form_data.append("name", name);
    form_data.append("email", email);
    form_data.append("subject", subject);
    form_data.append("message", message);
    form_data.append("honey", honey);

    xhr.open('POST', url)
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.onload = () =>{
      if(xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if(result.success){
          document.getElementById('message-box').style.display = "";
          document.getElementById('success_page').innerText = result.msg;
          document.getElementById('contactForm').reset();
          button.value = "Send message";
        }
        else {
          alert(result.msg);
        }
      }
    }
    xhr.send(form_data);
    return false;

    event.preventDefault();
  });
})
