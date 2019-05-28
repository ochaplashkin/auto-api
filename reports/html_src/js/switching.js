TIME_FOR_ANIMATION=100;
$('#overview').fadeIn(TIME_FOR_ANIMATION); 
$('table').fadeOut(TIME_FOR_ANIMATION); function getOverview(){$('table').fadeOut(TIME_FOR_ANIMATION); $('#overview').fadeIn(TIME_FOR_ANIMATION); $('overview-btn').addClass('active');
$('table-btn').removeClass('active');}function getTable(){$('#overview').fadeOut(TIME_FOR_ANIMATION); $('table').fadeIn(TIME_FOR_ANIMATION); $('overview-btn').removeClass('active'); 
$('table-btn').addClass('active');}