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
       alert("Picture size is too big!")
       return;
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

   else if (current_field == 'header') {
     var url = '/header/' + site_name;
     var header = document.getElementById('header').value;
     var subheader = document.getElementById('subheader').value;
     var editSeo = document.getElementById('editSeo');
     if (editSeo.checked) {
       var seo_title = document.getElementById('seo_title').value;
       var seo_desc = document.getElementById('seo_desc').value;
     }
     form_data.append("editSeo", editSeo.checked);
     form_data.append("seo_title", seo_title);
     form_data.append("seo_desc", seo_desc);
     form_data.append('header', header);
     form_data.append('subheader', subheader);
   }

   else if (current_field == 'social') {
     var url = '/socialblog/' + site_name;
     var twitter = document.getElementById('twitter').value;
     var facebook = document.getElementById('facebook').value;
     var instagram = document.getElementById('instagram').value;
     var github = document.getElementById('github').value;
     var youtube = document.getElementById('youtube').value;
     var linkedin = document.getElementById('linkedin').value;
     form_data.append('twitter', twitter);
     form_data.append('facebook', facebook);
     form_data.append('instagram', instagram);
     form_data.append('github', github);
     form_data.append('youtube', youtube);
     form_data.append('linkedin', linkedin);
   }

   xhr.open('POST', url)
   xhr.setRequestHeader("X-CSRFToken", csrf_token);
   xhr.onload = () =>{
     if(xhr.status == 200){
       $(this).text('Save Changes');
       const result = JSON.parse(xhr.responseText);
       if(result.success){
         if(result.current_field == 'acc_g'){
           alert(result.name);
           alert(result.filename);
           // Swal.fire({
           //  title: "Good job!",
           //  text: "Saved successfully!",
           //  type: "success",
           //  confirmButtonClass: 'btn btn-primary',
           //  buttonsStyling: false,
           // });
           $("html, body").animate({ scrollTop: 0 }, "slow");
         }
         else if(result.current_field == 'h'){
           saveHeader(result.header, result.subheader, result.header_id);
         }
         else if(result.current_field == 'so'){
           Swal.fire({
            title: "Good job!",
            text: "Saved successfully!",
            type: "success",
            confirmButtonClass: 'btn btn-primary',
            buttonsStyling: false,
           });
           $("html, body").animate({ scrollTop: 0 }, "slow");
         }
       }
       else{
         alert(result.msg);
       }
     }
   }
   xhr.send(form_data);
   return false;
 })
})
