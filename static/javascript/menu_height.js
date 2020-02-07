//This code is ment to adjust the height of the menu area as the screen width changes.
//This code is highly unrobust to changes in the menu items and should be refactored.
$( window ).on('load',
  function(){
    if($(".menu-elem").eq(3).width() < 100 || $( window ).width() <= 768){
      $(".buffer").height(90);
      $(".main").css("top","600px");
    }else{
      $(".buffer").height(40);
      $(".main").css("top","550px");
    }
  }
)
// console.log("hi");
// console.log($(".menu-elem").eq(3));
$(".menu-elem").eq(3).resize(function(e){console.log("hello")});
$( window ).resize(
  function(e){
    if($(".menu-elem").eq(3).width() < 100 || $( window ).width() <= 768){
      $(".buffer").height(90);
      $(".main").css("top","600px");
    }else{
      $(".buffer").height(40);
      $(".main").css("top","550px");
    }
    setTimeout(function(e){
      if($(".menu-elem").eq(3).width() < 100 || $( window ).width() <= 768){
        $(".buffer").height(90);
        $(".main").css("top","600px");
      }else{
        $(".buffer").height(40);
        $(".main").css("top","550px");
      }
    }, 500)
  }
);