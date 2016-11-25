RefreshPage = function() {
  setTimeout(function() {
    if ($('#autoRefresh').hasClass('refreshOn')) {
      location.reload();      
    } else {
      RefreshPage();
    }
    }, 30 * 1000);
}

$(document).ready(function(){
  $(".flip").click(function(){
    $(".panel:eq(" + $(this).index(".flip") + ")").slideToggle("fast");
  });
  $('#slideAll').click(function(){
  	if ($(this).hasClass('btnShow')) {
  		$(this).removeClass('btnShow');
  		$(this).text('展开');
	  	$('.panel').slideUp('fast');
  	} else {
  		$(this).addClass('btnShow');
  		$(this).text('收起');
	  	$('.panel').slideDown('fast');
  	}
  });
  if ($('.blackList').size() == 0) {
  	$('#slideAll').hide();
  } else {
  	$('#slideAll').show();
  }
  $('#autoRefresh').click(function(){
    if ($(this).hasClass('refreshOn')) {
      $(this).removeClass('refreshOn');
      $(this).text('开启');
    } else {
      $(this).addClass('refreshOn');
      $(this).text('关闭');
    }
  });
  RefreshPage()
});
