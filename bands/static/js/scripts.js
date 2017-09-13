
function loadResults(resultsContainer, url){
    if (url == null || url == '' || url.startsWith('#')){
        return;
    }
    resultsContainer.addClass('loading-container');
    $.get(url, {}, function(data){
        resultsContainer.find('.results').html(data);
        resultsContainer.removeClass('loading-container');
        window.history.replaceState({}, '', url);
    });
}

function loadPaginationAjax(){
    list.on('click', '.pagination a', function(e){
        e.preventDefault();
        if ($(this).parent().hasClass('active'))
            return;
        var url = $(this).attr('href')
        loadResults(list, url);
    });
}

$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    var searchForm = $('#searchForm');
    var url = searchForm.attr('action');
    var results = $("#results")

 /* $(".select2").on('change',function() {
    data = searchForm.serialize();
    results.load(url + '?' + data);
  });
*/
  $('#filter').on('click', function(e){
    e.preventDefault();
    data = searchForm.serialize();
    results.load(url + '?' + data);
  });

  $('#viewall').on('click', function(e){
    e.preventDefault();
    searchForm[0].reset();
    data = searchForm.serialize();
    results.load(url + '?' + data);
  });

    var $nav = $(".navbar-fixed-top");
    function navbarScroll(){
        $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.find('.navbar-header').height());
    }
    navbarScroll();
    $(document).scroll(navbarScroll);

    function formatTag (tag) {
      return tag;
    };

    $('a.smoothscroll').on('click', function(event) {
      var $anchor = $(this);
      $('html, body').stop().animate({
          scrollTop: $($anchor.attr('href')).offset().top
      }, 900);
      event.preventDefault();
  });

  $('.carousel').carousel({
        interval: 10000
    });

  var panelMaps = $('.panel .map');
  function resizeMaps(){
    panelMaps.each(function(){
        var panel = $(this).parents('.panel');
        if (panel.find('.size-check').is(':visible')){
            $(this).css('height', panel.innerHeight() + 'px');
        }
        else{
            $(this).css('height', 'auto');
        }
    });
  }
  if (panelMaps.size() > 0){
    resizeMaps();
    $(window).on('resize', resizeMaps);
  }

});





