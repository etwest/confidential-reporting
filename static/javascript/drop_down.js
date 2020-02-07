$( window ).on('load',function(){
  $("#cf2").click(function() {
    $("#cf2 img.top").toggleClass("transparent");
    $("#cf2 img.bottom").toggleClass("transparent");
    if($("#optional").hasClass("hiding")){
      $("#optional").slideDown(1000);
    }else{
      $("#optional").slideUp(1000);
    }
    $("#optional").toggleClass("hiding");
  });
});