/* scroll to bottom when pressing on button */
$(document).ready(function(){
$("#cite").click(function() {
 $('html, body').animate({ 
   scrollTop: $(document).height()-($(window).height())}, 
   1000, 
   "easeOutQuint"
);
});
});