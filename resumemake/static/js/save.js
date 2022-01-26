document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search)
  var site_id = params.get('site_id');

  $('.save').on('click', function(e){
   const xhr = new XMLHttpRequest();
   var current_field = $(this).attr('data');
   var csrf_token = document.getElementById('csrf_token').value;
   var form_data = new FormData();
   $(this).text('Saving...');

   if(current_field == "basic_info"){
     var url = '/basicinfo/' + site_id;
     var ins = document.getElementById('file').files.length;

     if(ins > 0) {
       var size = document.getElementById('file').files[0].size;
     }

     if(size > 2*1024*1024) {
       alert("Picture size is too big!")
       $(this).text('Save Changes');
       return false;
     }
     var FirstName = document.getElementById('FirstName').value;
     var LastName = document.getElementById('LastName').value;
     var email = document.getElementById('email').value;
     var phone = document.getElementById('phone').value;
     var tagline = document.getElementById('tagline').value;
     var birth_day = document.getElementById('birth_day').value;
     var country = document.getElementById('country').value;
     var city = document.getElementById('city').value;
     form_data.append("FirstName", FirstName);
     form_data.append("LastName", LastName);
     form_data.append("email", email);
     form_data.append("phone", phone);
     form_data.append("tagline", tagline);
     form_data.append("birth_day", birth_day);
     form_data.append("country", country);
     form_data.append("city", city);
     form_data.append("file", document.getElementById('file').files[0]);
   }

   else if(current_field == "introduction"){
     var url = '/introduction/' + site_id;
     var intro_title = document.getElementById('intro_title').value;
     var editor = document.querySelector('#editor-container');
     var introduction = editor.children[0].innerHTML;
     form_data.append("introduction", introduction);
     form_data.append("intro_title", intro_title);
   }

   else if(current_field == "social"){
     var url = '/social/' + site_id;
     var twitter = document.getElementById('twitter').value;
     var facebook = document.getElementById('facebook').value;
     var instagram = document.getElementById('instagram').value;
     var github = document.getElementById('github').value;
     var youtube = document.getElementById('youtube').value;
     var linkedin = document.getElementById('linkedin').value;
     form_data.append("twitter", twitter);
     form_data.append("facebook", facebook);
     form_data.append("instagram", instagram);
     form_data.append("github", github);
     form_data.append("youtube", youtube);
     form_data.append("linkedin", linkedin);
   }

   else if(current_field == "workExp"){
     var url = '/workExp/' + site_id;
     var position = document.getElementById('position').value;
     var company = document.getElementById('company').value;
     var start_month_job = document.getElementById('start_month_job').value;
     var start_year_job = document.getElementById('start_year_job').value;
     var end_month_job = document.getElementById('end_month_job').value;
     var end_year_job = document.getElementById('end_year_job').value;
     var desc_work = document.getElementById('desc_work').value;
     form_data.append('position', position);
     form_data.append('company', company);
     form_data.append('start_month_job', start_month_job);
     form_data.append('start_year_job', start_year_job);
     form_data.append('end_month_job', end_month_job);
     form_data.append('end_year_job', end_year_job);
     form_data.append('desc_work', desc_work);
   }

   else if(current_field == "service"){
     var url = '/service/' + site_id;
     var service_name = document.getElementById('service_name').value;
     var service_icon = document.getElementById('service_icon').value;
     var desc_service = document.getElementById('desc_service').value;

     if(!service_name || !desc_service){
       alert('Servis name and description are required fields');
       $(this).text('Save Changes');
       return false;
     }

     form_data.append("service_name", service_name);
     form_data.append("service_icon", service_icon);
     form_data.append('desc_service', desc_service);
   }

   else if(current_field == "port"){
     var url = '/portfolio/' + site_id;
     var ins = document.getElementById('port_pics').files.length;

     if(ins == 0) {
       alert("No image found");
       $(this).text('Save Changes');
       return false;
     }
     var project_name = document.getElementById('port_project_name').value;
     var website = document.getElementById('port_website').value;
     var creation_time = document.getElementById('port_creation_time').value;
     var desc_port = document.getElementById('desc_port').value;
     var tag = document.getElementById('tag').value; 
     form_data.append("project_name", project_name);
     form_data.append("website", website);
     form_data.append("creation_time", creation_time);
     form_data.append("tag", tag);
     form_data.append('desc_port', desc_port);
     form_data.append("ins", ins);
     for (i=0; i<ins; i++){
       form_data.append("port_pics"+i, document.getElementById('port_pics').files[i]);
     }
   }

   else if(current_field == "edu"){
     var url = '/edu/' + site_id;
     var field = document.getElementById('field').value;
     var school = document.getElementById('school').value;
     var start_month_edu = document.getElementById('start_month_edu').value;
     var start_year_edu = document.getElementById('start_year_edu').value;
     var end_month_edu = document.getElementById('end_month_edu').value;
     var end_year_edu = document.getElementById('end_year_edu').value;
     var desc_edu = document.getElementById('desc_edu').value;
     form_data.append('field', field);
     form_data.append('school', school);
     form_data.append('start_month_edu', start_month_edu);
     form_data.append('start_year_edu', start_year_edu);
     form_data.append('end_month_edu', end_month_edu);
     form_data.append('end_year_edu', end_year_edu);
     form_data.append('desc_edu', desc_edu);
   }

   else if(current_field == "course"){
     var url = '/course/' + site_id;
     var course_name = document.getElementById('course_name').value;
     var institution = document.getElementById('institution').value;
     var start_month_course = document.getElementById('start_month_course').value;
     var start_year_course = document.getElementById('start_year_course').value;
     var end_month_course = document.getElementById('end_month_course').value;
     var end_year_course = document.getElementById('end_year_course').value;
     var desc_course = document.getElementById('editor-course').value;
     form_data.append('course_name', course_name);
     form_data.append('institution', institution);
     form_data.append('start_month_course', start_month_course);
     form_data.append('start_year_course', start_year_course);
     form_data.append('end_month_course', end_month_course);
     form_data.append('end_year_course', end_year_course);
     form_data.append('desc_course', desc_course);
   }

   else if(current_field == "skill"){
     var url = '/skill/' + site_id;
     var skill = document.getElementById('skill').value;
     var level = document.getElementById('level').value;
     var category = document.getElementById('sk_category').value;
     form_data.append('skill', skill);
     form_data.append('level', level);
     form_data.append('category', category);
   }

   else if(current_field == "lang"){
     var url = '/language/' + site_id;
     var lang = document.getElementById('lang').value;
     var level = document.getElementById('lang_level').value;

     if (!lang || !level){
      Swal.fire({
        title: "Error!",
        text: 'Fields are required!',
        type: "error",
        confirmButtonClass: 'btn btn-danger',
        buttonsStyling: false,
       });
       $("html, body").animate({ scrollTop: 0 }, "slow");
       $(this).text('Save Changes');
       return false;
     }
     if(parseInt(level) > 100 || parseInt(level) < 1 ){
      Swal.fire({
        title: "Error!",
        text: 'Level should be between 1 and 100!',
        type: "error",
        confirmButtonClass: 'btn btn-danger',
        buttonsStyling: false,
       });
       $("html, body").animate({ scrollTop: 0 }, "slow");
       $(this).text('Save Changes');
       return false;
     }

     form_data.append('lang', lang);
     form_data.append('level', level);
   }

   else if(current_field == "testi"){
     var url = '/testimonials/' + site_id;
     var ins = document.getElementById('testi_pic').files.length;

     if(ins == 0) {
       alert("No image found");
       $(this).text('Save Changes');
       return false;
     }
     var name = document.getElementById('tested_name').value;
     var company = document.getElementById('com_occ').value;
     var desc_testi = document.getElementById('desc_testi').value;
     form_data.append("name", name);
     form_data.append("company", company);
     form_data.append("testi_pic", document.getElementById('testi_pic').files[0]);
     form_data.append('desc_testi', desc_testi);
   }

   else if(current_field == "site_settings"){
    var url = '/site_settings/' + site_id;
    var pdf_resume = document.getElementById('pdf_resume');
    var contact_notify = document.getElementById('contact_notify');
    var download_notify = document.getElementById('download_notify');

    var ins = pdf_resume.files.length;

     if(ins > 0) {
       var size = pdf_resume.files[0].size;
     }

     if(size > 2*1024*1024) {
       alert("File size is too big! Max 2MB allowed");
       $(this).text('Save Changes');
       return false;
     }

    if(document.getElementById('background_image') !== null){
      var background_image = document.getElementById('background_image');

      var ins = background_image.files.length;

      if(ins > 0) {
       var size = background_image.files[0].size;
      }

      if(size > 2*1024*1024) {
       alert("File size is too big! Max 2MB allowed");
       $(this).text('Save Changes');
       return false;
      }
      form_data.append("background_image", background_image.files[0]);
    }

    form_data.append("contact_notify", contact_notify.checked);
    form_data.append("download_notify", download_notify.checked);
    form_data.append("pdf_resume", pdf_resume.files[0]);
  }

   xhr.open('POST', url)
   xhr.setRequestHeader("X-CSRFToken", csrf_token);
   xhr.onload = () =>{
     if(xhr.status == 200){
       $(this).text('Save Changes');
       const result = JSON.parse(xhr.responseText);
       if(result.success){
         if(result.current_field == 's'){
           saveSkill(result.skill, result.level, result.category, result.skill_id);
         }
         else if(result.current_field == 'b'){
           Swal.fire({
            title: "Good job!",
            text: "Saved successfully!",
            type: "success",
            confirmButtonClass: 'btn btn-primary',
            buttonsStyling: false,
           });
           $("html, body").animate({ scrollTop: 0 }, "slow");
         }
         else if(result.current_field == 'i'){
           Swal.fire({
            title: "Good job!",
            text: "Saved successfully!",
            type: "success",
            confirmButtonClass: 'btn btn-primary',
            buttonsStyling: false,
           });
           $("html, body").animate({ scrollTop: 0 }, "slow");
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
         else if(result.current_field == 'w'){
           saveWorkExp(result.position, result.company, result.workExp_id, result.duration);
         }
         else if(result.current_field == 'p'){
           savePort(result.project_name, result.port_id);
         }
         else if(result.current_field == 'e'){
           saveEdu(result.field, result.school, result.edu_id, result.duration);
         }
         else if(result.current_field == 'c'){
           saveCourse(result.course_name, result.institution, result.course_id, result.duration);
         }
         else if(result.current_field == 'l'){
           saveLang(result.lang, result.level, result.lang_id);
         }
         else if(result.current_field == 'se'){
           saveService(result.service_name, result.service_id);
         }
         else if(result.current_field == 't'){
           saveTesti(result.name, result.company, result.testi_id);
         }
         else if(result.current_field == 'ss'){
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
        Swal.fire({
          title: "Error!",
          text: result.msg,
          type: "error",
          confirmButtonClass: 'btn btn-danger',
          buttonsStyling: false,
         });
         $("html, body").animate({ scrollTop: 0 }, "slow");
       }
     }
   }
   xhr.send(form_data);
   return false;
  })

  function saveSkill(skill, level, category, skill_id){
    var skill_table = document.getElementById('skill_table');
    var form_skill = document.getElementById('form_skill');
    var addAnother = document.getElementById("addAnotherSkill");
    if (skill_table.style.display == 'none'){
      skill_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_skill');
    tbody.innerHTML += '<tr class="table-active" id=s_' + skill_id + '>' +
      '<td>' +
        '<span class="font-weight-bold">' + skill + '</span>' +
      '</td>' +
      '<td>' + level + '</td>' +
      '<td>' + category + '</td>' +
      '<td>' +
        '<i class="fa fa-trash-o deleteItem" data=s_' + skill_id + '></i>' +
      '</td>' +
    '</tr>';

    form_skill.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_skill.style.display = "block";
      addAnother.style.display = "none";
    })
    $("html, body").animate({ scrollTop: 0 }, "slow");
    $("#reset_skill").click();
    return false;
  }

  function saveLang(lang, level, lang_id){
    var lang_table = document.getElementById('lang_table');
    var form_lang = document.getElementById('form_lang');
    var addAnother = document.getElementById("addAnotherLang");
    if (lang_table.style.display == 'none'){
      lang_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_lang');
    tbody.innerHTML += '<tr class="table-active" id=l_' + lang_id + '>' +
      '<td>' +
        '<span class="font-weight-bold">' + lang + '</span>' +
      '</td>' +
      '<td>' + level + '</td>' +
      '<td>' +
        '<i class="fa fa-trash-o deleteItem" data=l_' + lang_id + '></i>' +
      '</td>' +
    '</tr>';

    form_lang.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_lang.style.display = "block";
      addAnother.style.display = "none";
    })
    $("html, body").animate({ scrollTop: 0 }, "slow");
    $("#reset_lang").click();
    return false;
  }

  function saveWorkExp(position, company, workExp_id, duration){
    var workExp_table = document.getElementById('workExp_table');
    var form_workexp = document.getElementById('form_workexp');
    var addAnother = document.getElementById("addAnotherWork");
    if (workExp_table.style.display == 'none'){
      workExp_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_work');
    tbody.innerHTML += '<tr class="table-active" id=w_' + workExp_id + '>' +
      '<td>' +
        '<span class="font-weight-bold">' + position + '</span>' +
      '</td>' +
      '<td>' + company + '</td>' +
      '<td>' +
        duration +
      '</td>' +
      '<td>' +
        '<i class="fa fa-trash-o deleteItem" data=w_' + workExp_id + '></i>' +
      '</td>' +
    '</tr>';

    form_workexp.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_workexp.style.display = "block";
      addAnother.style.display = "none";
    })
    $("html, body").animate({ scrollTop: 0 }, "slow");
    $('#reset_workexps').click();
    return false;
  }

  function saveService(service_name, service_id){
    var service_table = document.getElementById('service_table');
    var form_service = document.getElementById('form_service');
    var addAnother = document.getElementById("addAnotherService");
    if (service_table.style.display == 'none'){
      service_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_service');
    tbody.innerHTML += '<tr class="table-active" id=se_' + service_id + '>' +
      '<td>' +
        '<span class="font-weight-bold">' + service_name + '</span>' +
      '</td>' +
      '<td>' +
        '<i class="fa fa-trash-o deleteItem" data=se_' + service_id + '></i>' +
      '</td>' +
    '</tr>';

    form_service.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_service.style.display = "block";
      addAnother.style.display = "none";
    })
    $("html, body").animate({ scrollTop: 0 }, "slow");
    return false;
  }

  function saveTesti(name, company, testi_id){
    var testi_table = document.getElementById('testi_table');
    var form_testi = document.getElementById('form_testi');
    var addAnother = document.getElementById("addAnotherTesti");
    if (testi_table.style.display == 'none'){
      testi_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_testi');
    tbody.innerHTML += '<tr class="table-active" id=t_' + testi_id + '>' +
      '<td>' +
        '<span class="font-weight-bold">' + name + '</span>' +
      '</td>' +
      '<td>' + company + '</td>' +
      '<td>' +
        '<i class="fa fa-trash-o deleteItem" data=t_' + testi_id + '></i>' +
      '</td>' +
    '</tr>';

    form_testi.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_testi.style.display = "block";
      addAnother.style.display = "none";
    })
    $("html, body").animate({ scrollTop: 0 }, "slow");
    $('#reset_testi').click();
    return false;
  }

  function savePort(project_name, port_id){
    var port_table = document.getElementById('port_table');
    var form_port = document.getElementById('form_port');
    var addAnother = document.getElementById("addAnotherPort");
    if (port_table.style.display == 'none'){
      port_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_port');
    tbody.innerHTML += '<tr class="table-active" id=p_' + port_id + '>' +
      '<td>' +
        '<span class="font-weight-bold">' + project_name + '</span>' +
      '</td>' +
      '<td>' +
        '<i class="fa fa-trash-o deleteItem" data=p_' + port_id + '></i>' +
      '</td>' +
    '</tr>';

    form_port.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_port.style.display = "block";
      addAnother.style.display = "none";
    })
    $("html, body").animate({ scrollTop: 0 }, "slow");
    $("#reset_port").click();
    return false;
  }

  function saveEdu(field, school, edu_id, duration){
    var edu_table = document.getElementById('edu_table');
    var form_edu = document.getElementById('form_edu');
    var addAnother = document.getElementById("addAnotherEdu");
    if (edu_table.style.display == 'none'){
      edu_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_edu');
    tbody.innerHTML += '<tr class="table-active" id=e_' + edu_id + '>' +
      '<td>' +
        '<span class="font-weight-bold">' + field + '</span>' +
      '</td>' +
      '<td>' + school + '</td>' +
      '<td>' +
        duration +
      '</td>' +
      '<td>' +
        '<i class="fa fa-trash-o deleteItem" data=e_' + edu_id + '></i>' +
      '</td>' +
    '</tr>';

    form_edu.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_edu.style.display = "block";
      addAnother.style.display = "none";
    })
    $("html, body").animate({ scrollTop: 0 }, "slow");
    $("#reset_edu").click();
    return false;
  }

  function saveCourse(course_name, institution, course_id, duration){
    var course_table = document.getElementById('course_table');
    var form_course = document.getElementById('form_course');
    var addAnother = document.getElementById("addAnotherCourse");
    if (course_table.style.display == 'none'){
      course_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_course');
    tbody.innerHTML += '<tr class="table-active" id=c_' + course_id + '>' +
      '<td>' +
        '<span class="font-weight-bold">' + course_name + '</span>' +
      '</td>' +
      '<td>' + institution + '</td>' +
      '<td>' +
        duration +
      '</td>' +
      '<td>' +
        '<i class="fa fa-trash-o deleteItem" data=c_' + course_id + '></i>' +
      '</td>' +
    '</tr>';

    form_course.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_course.style.display = "block";
      addAnother.style.display = "none";
    })
    $("html, body").animate({ scrollTop: 0 }, "slow");
    return false;
  }

  $(".connect-domain").click(function( event ) {
    const xhr = new XMLHttpRequest();
    var domain = document.getElementById('domain').value;
    var csrf_token = document.getElementById('csrf_token').value;
    var form_data = new FormData();
    form_data.append('domain', domain);
    url = '/connect_resume_domain/' + site_id;

    $(this).text('Connecting...');

    xhr.open('POST', url)
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.onload = () =>{
      if(xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if(result.success){
          document.getElementById('domain_result').style.display = "";
          document.getElementById('DomainConnected').innerText = "https://" + domain;
          document.getElementById('point').innerText = "46.101.5.43";
          Swal.fire({
           icon: 'success',
           title: "Domain Connected!",
           text: "Set A record of your domain to 43.101.5.43",
           type: "success",
           confirmButtonClass: 'btn btn-primary',
           buttonsStyling: false,
          });
          $(this).text('Connect');
        }
        else {
          Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Invalid url!',
          })
          $(this).text('Connect');
        }
      }
    }
    xhr.send(form_data);
  })

  $(".dns_status").click(function( event ) {
    const xhr = new XMLHttpRequest();
    url = '/check_dns_status/' + site_id;

    $(this).text('Checking...');

    xhr.open('GET', url)
    xhr.onload = () =>{
      if(xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if(result.success){
          Swal.fire({
           icon: 'success',
           title: "Domain Connected!",
           text: "Domain connected to our servers",
           type: "success",
           confirmButtonClass: 'btn btn-primary',
           buttonsStyling: false,
          });
          $(this).text('Done');
        }
        else {
          Swal.fire({
            icon: 'error',
            title: 'Connection pending',
            text: result.msg,
          })
          $(this).text('Check Status');
        }
      }
    }
    xhr.send();
  })

  
 document.addEventListener('click', deleteItem);
 function deleteItem(e){
   if (e.target.matches('.deleteItem')){
     const request = new XMLHttpRequest();
     var csrf_token = document.getElementById('csrf_token').value;
     var type_id = $(e.target).attr('data');
     var data = {"type_id": type_id};
     var url = '/deleteItem/' + site_id;

     request.open('POST', url);
     request.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
     request.setRequestHeader("X-CSRFToken", csrf_token);
     request.onload = () =>{
       if (request.status == 200){
         const result = JSON.parse(request.responseText);
         if(result.success){
           if (result.current_field == "w"){
             var tbody = document.getElementById('tbody_work');
             var item = document.getElementById(type_id);
             item.parentNode.removeChild(item);
             if (tbody.childElementCount == 0){
               var workExp_table = document.getElementById('workExp_table');
               workExp_table.style.display = "none";
             }
             e.preventDefault();
           }

           else if (result.current_field == "se"){
             var tbody = document.getElementById('tbody_service');
             var item = document.getElementById(type_id);
             item.parentNode.removeChild(item);
             if (tbody.childElementCount == 0){
               var service_table = document.getElementById('service_table');
               service_table.style.display = "none";
             }
             e.preventDefault();
           }

           else if (result.current_field == "p"){
             var tbody = document.getElementById('tbody_port');
             var item = document.getElementById(type_id);
             item.parentNode.removeChild(item);
             if (tbody.childElementCount == 0){
               var port_table = document.getElementById('port_table');
               port_table.style.display = "none";
             }
             e.preventDefault();
           }

           else if (result.current_field == "t"){
             var tbody = document.getElementById('tbody_testi');
             var item = document.getElementById(type_id);
             item.parentNode.removeChild(item);
             if (tbody.childElementCount == 0){
               var testi_table = document.getElementById('testi_table');
               testi_table.style.display = "none";
             }
             e.preventDefault();
           }

           else if(result.current_field == "e"){
             var tbody = document.getElementById('tbody_edu');
             var item = document.getElementById(type_id);
             item.parentNode.removeChild(item);
             if (tbody.childElementCount == 0){
               var edu_table = document.getElementById('edu_table');
               edu_table.style.display = "none";
             }
             e.preventDefault();
           }

           else if(result.current_field == "c"){
             var tbody = document.getElementById('tbody_course');
             var item = document.getElementById(type_id);
             item.parentNode.removeChild(item);
             if (tbody.childElementCount == 0){
               var course_table = document.getElementById('course_table');
               course_table.style.display = "none";
             }
             e.preventDefault();
           }

           else if(result.current_field == "s"){
             var tbody = document.getElementById('tbody_skill');
             var item = document.getElementById(type_id);
             item.parentNode.removeChild(item);
             if (tbody.childElementCount == 0){
               var skill_table = document.getElementById('skill_table');
               skill_table.style.display = "none";
             }
             e.preventDefault();
           }

           else if(result.current_field == "l"){
             var tbody = document.getElementById('tbody_lang');
             var item = document.getElementById(type_id);
             item.parentNode.removeChild(item);
             if (tbody.childElementCount == 0){
               var lang_table = document.getElementById('lang_table');
               lang_table.style.display = "none";
             }
             e.preventDefault();
           }
         }
         else{
           alert("Lutfen giriş yapınız");
         }
       }
     }
     request.send(JSON.stringify(data));
     return false;
   }
 }

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
})
