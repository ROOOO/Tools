$(document).ready(function(){
  $(".flip").click(function(){
    $(".panel:eq(" + $(this).index(".flip") + ")").slideToggle("fast");
  });
  $('#slideAll').click(function(){
  	if ($(this).hasClass('btnShow')) {
  		$(this).removeClass('btnShow');
  		$(this).text('收起');
	  	$('.panel').slideUp('fast');
  	} else {
  		$(this).addClass('btnShow');
  		$(this).text('展开');
	  	$('.panel').slideDown('fast');
  	}
  });
});
