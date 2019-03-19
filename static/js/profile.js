$(document).ready(function(){
$("#show").click(function() {
 $('html, body').animate({ 
   scrollTop: $(document).height()-($(window).height()/2)}, 
   2000, 
   "easeOutQuint"
);
});
});
