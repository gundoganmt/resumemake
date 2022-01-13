document.addEventListener('DOMContentLoaded', () => {
  $(".accept").click(function( event ) {
   const xhr = new XMLHttpRequest();
   var blog_id = $(this).attr('data');
   var csrf_token = document.getElementById('csrf_token').value;
   var form_data = new FormData();
   form_data.append('blog_id', blog_id);
   url = '/accept-authorship';

   xhr.open('POST', url)
   xhr.setRequestHeader("X-CSRFToken", csrf_token);
   xhr.onload = () =>{
     if(xhr.status == 200){
       const result = JSON.parse(xhr.responseText);
       if(result.success){
         Swal.fire({
          title: "Good job!",
          text: "congratulations! You are author of " + result.site_name,
          type: "success",
          confirmButtonClass: 'btn btn-primary',
          buttonsStyling: false,
         });
         $("html, body").animate({ scrollTop: 0 }, "slow");
         $(this).text('Added');
       }
       else {
         alert(result.msg);
       }
     }
   }
   xhr.send(form_data);
 })
})
