
// some javascript that highlights the active tab when selected based on urls
$(document).ready(function(){
    var current = location.pathname;
    $('#selectable li a').each(function(){
        var $this = $(this);
        if($this.attr('href') == current){
            $this.addClass('active');
        }
    });
});

$(document).ready(function(){
    $( document ).tooltip();
  } );