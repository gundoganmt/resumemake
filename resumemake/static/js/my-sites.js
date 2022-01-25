document.addEventListener('DOMContentLoaded', () => {
  searchbox = document.getElementById('search');
  $('#allSites').on('click', function(e){
    searchbox.value = '';
    $('#search').keyup();
  });

  $('#publishedSites').on('click', function(e){
    searchbox.value = 'published';
    $('#search').keyup();
    searchbox.value = '';
  });

  $('#savedSites').on('click', function(e){
    searchbox.value = 'draft';
    $('#search').keyup();
    searchbox.value = '';
  });

  $('#resumeSites').on('click', function(e){
    resume_sites = document.getElementsByName('ResumeSite');
    resume_sites.forEach(function(r){
      r.style.display = '';
    })

  });

});
