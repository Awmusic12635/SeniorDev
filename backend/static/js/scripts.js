$(document).ready(function(){
    if(window.location.href.indexOf("dashboard") > -1) {
      $('#dashboard-li').addClass('active');
    } else if(window.location.href.indexOf("item") > -1) {
      $('#items-li').addClass('active');
    } else if(window.location.href.indexOf("category") > -1) {
      $('#items-li').addClass('active');
    } else if(window.location.href.indexOf("checkout") > -1) {
      $('#checkout-li').addClass('active');
    } else if(window.location.href.indexOf("checkin") > -1) {
      $('#checkin-li').addClass('active');
    } else if(window.location.href.indexOf("reservationRequest") > -1) {
      $('#reservations-li').addClass('active');
    } else if(window.location.href.indexOf("reservation") > -1) {
      $('#reservations-li').addClass('active');
    }
});