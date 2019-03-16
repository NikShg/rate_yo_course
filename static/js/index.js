/* Hide the search box and cancel link on page load, if search button pressed, reveal input box and cancel link */
$(document).ready(function(){
	$("#search-form").hide();
	$("#cancel-link").hide();
	$("#show").click(function(){
		$("#search-form").show();
		$("#cancel-link").show();
		$("#show").hide();
		});
	$("#cancel-link").click(function(){
		$("#search-form").hide();
		$("#cancel-link").hide();
		$("#show").show();
			});
});

  $( function() {
    $( document ).tooltip();
  } );
  
/* Autocomplete suggestions */ 
$(document).ready(function(){
	var availableTags = ["glasgow", "edinburgh"];
    $( '#input' ).autocomplete({
      source: availableTags,
	  messages: {
        noResults: '',
        results: function() {}
    }
    })
	
	$("#input").autocomplete({focus:function(e,ui) {
        return false;
    }});
  });
    
/* Making autocomplete suggestions box the same size as the input box */
jQuery.ui.autocomplete.prototype._resizeMenu = function () {
  var ul = this.menu.element;
  ul.outerWidth(this.element.outerWidth());
}
