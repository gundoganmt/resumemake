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
    searchbox.value = 'saved';
    $('#search').keyup();
    searchbox.value = '';
  });

  $('#blogSites').on('click', function(e){
    blog_sites = document.getElementsByName('BlogSite');
    blog_sites.forEach(function(b){
      b.style.display = '';
    })

    resume_sites = document.getElementsByName('ResumeSite');
    resume_sites.forEach(function(r){
      r.style.display = 'none';
    })
  });

  $('#resumeSites').on('click', function(e){
    resume_sites = document.getElementsByName('ResumeSite');
    resume_sites.forEach(function(r){
      r.style.display = '';
    })

    blog_sites = document.getElementsByName('BlogSite');
    blog_sites.forEach(function(b){
      b.style.display = 'none';
    })
  });

  $('#authorSites').on('click', function(e){
    searchbox.value = 'author';
    $('#search').keyup();
    searchbox.value = '';
  });

});
