
function loadResults(resultsContainer, url){
    if (url == null || url == '' || url.startsWith('#')){
        return;
    }
    resultsContainer.addClass('loading-container');
    $.get(url, {}, function(data){
        resultsContainer.find('.results').html(data);
        resultsContainer.removeClass('loading-container');
        var preserveHistory = resultsContainer.attr('data-preservehistory');
        console.log(preserveHistory);
        if (!preserveHistory || preserveHistory != 'true')
            window.history.replaceState({}, '', url);
    });
}

function loadPaginationAjax(list){
    var initialUrl = list.attr('data-initial');
    if ((initialUrl != null) && (initialUrl!='')){
        loadResults(list, initialUrl);
    }

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

  var panelMaps = $('.panel .map:not(.no-resize)');
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


  $(".image-field").each(function(){
        var field = $(this);
        var target = field.attr('data-ref');
        var type = field.attr('data-ref-type');
        console.log(type);
        field.find('input').on('change', function(){
            var input = this;
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    if (type == 'image'){
                        $(target).attr('src', e.target.result);
                    }
                    else{
                        $(target).css('background-image', 'url(' + e.target.result + ')');
                    }
                }
                reader.readAsDataURL(input.files[0]);
            }
        });
    });


});





