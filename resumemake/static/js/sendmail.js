document.addEventListener('DOMContentLoaded', () => {
  $(".contact-form").submit(function( event ) {
    const xhr = new XMLHttpRequest();
    var username = $(this).attr('data');
    var csrf_token = document.getElementById('csrf_token').value;
    var form_data = new FormData();
    url = '/usermails/' + username;

    button = document.getElementById('msg-btn');
    button.value = "Sending...";

    var full_name = document.getElementById('full_name').value;
    var email = document.getElementById('email').value;
    var subject = document.getElementById('subject').value;
    var content = document.getElementById('content').value;
    form_data.append("full_name", full_name);
    form_data.append("email", email);
    form_data.append("subject", subject);
    form_data.append("content", content);

    xhr.open('POST', url)
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.onload = () =>{
      if(xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if(result.success){
          Swal.fire({
           title: "Thank You!",
           text: "Message Sent Successfully!",
           type: "success",
           confirmButtonClass: 'btn btn-primary',
           buttonsStyling: false,
          });
          document.getElementById('contact-form').reset();
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
