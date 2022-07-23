'use strict';

$(function(){
    $(".button").on("click",function() {
        $(".box").slideToggle();
    });
});

$(function(){
    $(".tab").on("click",function(){
        var i=$(this).index()+1;
        $(".box").removeClass("active");
        $(".box").eq(i).addClass("active");
    });
});

$(function(){
    $(window).on('load scroll',function(){
        var winScroll=$(window).scrollTop();
        var winHeight=$(window).height();
        var scrollpos=winScroll+(winHeight*0.8);

        $(".show").each(function(){
            if($(this).offset().top<scrollPos){
                $(this).css({opacity:1,transform:'translate(0, 0)'});
            }
        });
    });
});