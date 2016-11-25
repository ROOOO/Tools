$(document).ready(function(){
  var RefreshPage = function() {
    setTimeout(function() {
      if ($('#autoRefresh').hasClass('refreshOn') && $('#filterInput').val() == '') {
        location.reload();    
      } else {
        RefreshPage();
      }
      }, 30 * 1000);
  }

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
  $('#filterInput').keyup(function(e){
    var val = $(this).val();
    // $('#keycount').text(val.length);
    $('label').each(function(){
      if (val == '') {
        $(this).show();
        return;
      }

      var classStr = $(this).attr('class').split(';');
      for (var i = 0; i < classStr.length; i++) {
        if ((e.which != 13 && classStr[i].substring(0, val.length) == val) || (e.which == 13 && classStr[i] == val)) {
          $(this).show();
          if (e.which == 13) {
            return;
          }
        } else {
          $(this).hide();
        }
      }
    });
  });

  var tasks = $('#todoListTask').text().split(',');
  var todoListTask = '';
  for (var i = 0; i < tasks.length; i++) {
    todoListTask += ('<b>' + tasks[i] + '</b>&nbsp;&nbsp;&nbsp;&nbsp;')
  }
  $('#todoListTask').html(todoListTask);

  RefreshPage()
});
