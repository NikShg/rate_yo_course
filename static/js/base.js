
// some jquery that highlights the active tab when selected based on urls
$(document).ready(function(){
    var current = location.pathname;
    $('#selectable li a').each(function(){
        var $this = $(this);
        if($this.attr('href') == current){
            $this.addClass('active');
        }
    });
});

// some jquery for the tooltips and welcome message in index page
$(document).ready(function(){
    $( document ).tooltip();
		$(".welcome").fadeOut(5000);
  } );