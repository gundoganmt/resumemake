document.addEventListener('DOMContentLoaded', () => {
  $('.save').on('click', function(e){
   const xhr = new XMLHttpRequest();
   var current_field = $(this).attr('data');
   var csrf_token = document.getElementById('csrf_token').value;
   var form_data = new FormData();
   $(this).text('Saving...');

   if(current_field == "accountGeneral"){
     var url = '/accountGeneral';
     var ins = document.getElementById('file').files.length;

     if(ins > 0) {
       var size = document.getElementById('file').files[0].size;
     }

     if(size > 2*1024*1024) {
       alert("Picture size is too big! 2Mb max")
       $(this).text('Save Changes');
       return false;
     }
     var name = document.getElementById('account-name').value;
     var surname = document.getElementById('account-surname').value;
     var email = document.getElementById('account-e-mail').value;
     var username = document.getElementById('username').value;
     var account_desc = document.getElementById('account_desc').value;

     form_data.append("name", name);
     form_data.append("surname", surname);
     form_data.append("email", email);
     form_data.append("username", username);
     form_data.append("account_desc", account_desc);
     form_data.append("file", document.getElementById('file').files[0]);
   }

   else if (current_field == 'changePass') {
     var url = '/changePass';
     var old_pass = document.getElementById('old_pass').value;
     var new_pass = document.getElementById('new_pass').value;
     var retype_pass = document.getElementById('retype_pass').value;

     form_data.append("old_pass", old_pass);
     form_data.append("new_pass", new_pass);
     form_data.append("retype_pass", retype_pass);
   }

   xhr.open('POST', url)
   xhr.setRequestHeader("X-CSRFToken", csrf_token);
   xhr.onload = () =>{
     if(xhr.status == 200){
       $(this).text('Save Changes');
       const result = JSON.parse(xhr.responseText);
       if(result.success){
         if(result.current_field == 'acc_g'){
           Swal.fire({
            title: "Good job!",
            text: "Saved successfully!",
            type: "success",
            confirmButtonClass: 'btn btn-primary',
            buttonsStyling: false,
           });
           $("html, body").animate({ scrollTop: 0 }, "slow");
         }
         else if(result.current_field == 'cp'){
          Swal.fire({
            title: "Good job!",
            text: "Password changed!",
            type: "success",
            confirmButtonClass: 'btn btn-primary',
            buttonsStyling: false,
           });
           $("html, body").animate({ scrollTop: 0 }, "slow");
         }
       }
       else{
        Swal.fire({
          icon: 'error',
          title: 'Error occured',
          text: result.msg,
        })
        $(this).text('Save Changes');
       }
     }
   }
   xhr.send(form_data);
   return false;
 })

 $(document).ready(function() {
  var readURL = function(input) {
      if (input.files && input.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
              $('.profile-pic').attr('src', e.target.result);
          }
          reader.readAsDataURL(input.files[0]);
      }
  }

  $(".file-upload").on('change', function(){
      readURL(this);
  });

  $(".upload-button").on('click', function() {
     $(".file-upload").click();
  });
});
})
