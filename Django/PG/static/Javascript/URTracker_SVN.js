RefreshPage = function() {
  setTimeout(function() {
    if ($('#autoRefresh').hasClass('refreshOn') && $('#input').text() == '') {
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
  $('#input').keyup(function(){
    var val = $(this).val();
    // $('#keycount').text(val.length);
    $('label').each(function(){
      var classStr = $(this).attr('class').split(';');
      for (var i = 0; i < classStr.length; i++) {
        if (!(classStr[i].substring(0, val.length) == val) && val != '') {
          $(this).hide();
        } else {
          $(this).show();
        }
      }
    });
  });

  var tasks = $('#todoListTask').text().split(',');
  var todoListTask = '';
  for (var i = 0; i < tasks.length; i++) {
    todoListTask += ('<b>' + tasks[i] + '</b>&nbsp;&nbsp;&nbsp;&nbsp;')
  }
  $('#todoListTask').html(todoListTask)

  RefreshPage()
});
