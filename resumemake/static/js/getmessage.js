document.addEventListener('DOMContentLoaded', () => {
  msg = document.getElementsByName('getmessage');
  msg.forEach(function(m){
    m.onclick = () => {
      const request = new XMLHttpRequest();
      var mail_id = parseInt(m.getAttribute('data'));
      var url = '/get-message/' + mail_id;
      request.open('GET', url);

      if(request.readyState){
        document.getElementById('subject').innerText = "loading...";
        document.getElementById('content').innerText = "";
      }

      request.onload = () =>{
        if (request.status == 200){
          const mail_data = JSON.parse(request.responseText);
          if(mail_data.success){
            document.getElementById('subject').innerText = mail_data.subject;
            document.getElementById('content').innerText = mail_data.content;
          }
          else {
            document.getElementById('subject').innerText = mail_data.msg;
            document.getElementById('content').innerText = "";
          }
        }
      }

      request.onerror = () =>{
        document.getElementById('subject').innerText = "Some thing went wrong! Refresh page and try again.";
        document.getElementById('content').innerText = "";
      }

      request.send();
    }
  })

  msg = document.getElementsByName('deletemessage');
  msg.forEach(function(m){
    m.onclick = () => {
      Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if (result.isConfirmed) {
          const request = new XMLHttpRequest();
          var mail_id = parseInt(m.getAttribute('data'));
          var url = '/delete-message/' + mail_id;
          request.open('GET', url);

          request.onload = () =>{
            if (request.status == 200){
              const mail_data = JSON.parse(request.responseText);
              if(mail_data.success){
                var tr = document.getElementById('m_'+mail_id);
                tr.parentNode.removeChild(tr);
                Swal.fire(
                  'Deleted!',
                  'Your file has been deleted.',
                  'success'
                )
              }
              else{
                Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: mail_data.msg,
                })
              }
            }
          }
          request.onerror = () =>{
            Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'Something went wrong! Refresh the page try again.',
            })
          }
          request.send();
        }
      })
    }
  })

})
