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
      