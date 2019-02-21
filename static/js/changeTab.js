/**
 * Created by guocheng on 2019/2/19.
 */
function checkMessage() {
            if($('div.active textarea').val()===''){
                $('div.active .button').attr("disabled",true);
                $('div.active .button').css("background-color","#c0c0c0");
            }
            else{
                $('div.active .button').attr("disabled",false);
                $('div.active .button').css("background-color","#4285f4");
            }
            if($('div.tab').not('.active').find('textarea').val()===''){
                $('div.tab').not('.active').find('.button').attr("disabled",true);
                $('div.tab').not('.active').find('.button').css("background-color","#c0c0c0");
            }
            else{
                $('div.tab').not('.active').find('.button').attr("disabled",false);
                $('div.tab').not('.active').find('.button').css("background-color","#4285f4");
            }
        }

$(document).ready(function () {
            var activePos = $('.tabs-header .active').position();
            function changePos() {
                activePos = $('.tabs-header .active').position();
                $('.border').stop().css({
                    left: activePos.left,
                    width: $('.tabs-header .active').width()
                });
                checkMessage();
            }
            changePos();

            function changeTab() {
                var getTabId = $('.tabs-header .active a').attr('tab-id');
                $('.tab').stop().fadeOut(300, function () {
                    $(this).removeClass('active');
                }).hide();
                $('.tab[tab-id=' + getTabId + ']').stop().fadeIn(300, function () {
                    $(this).addClass('active');
                });
            }
            $('.tabs-header a').on('click', function (e) {
                e.preventDefault();
                var tabId = $(this).attr('tab-id');
                $('.tabs-header a').stop().parent().removeClass('active');
                $(this).stop().parent().addClass('active');
                changePos();
                tabCurrentItem = tabItems.filter('.active');
                $('.tab').stop().fadeOut(300, function () {
                    $(this).removeClass('active');
                }).hide();
                $('.tab[tab-id="' + tabId + '"]').stop().fadeIn(300, function () {
                    $(this).addClass('active');
                });
            });
            var tabItems = $('.tabs-header ul li');
            var tabCurrentItem = tabItems.filter('.active');

            $('[ripple]').on('click', function (e) {
                var rippleDiv = $('<div class="ripple" />'), rippleOffset = $(this).offset(), rippleY = e.pageY - rippleOffset.top, rippleX = e.pageX - rippleOffset.left, ripple = $('.ripple');
                rippleDiv.css({
                    top: rippleY - ripple.height() / 2,
                    left: rippleX - ripple.width() / 2,
                    background: $(this).attr('ripple-color')
                }).appendTo($(this));
                window.setTimeout(function () {
                    rippleDiv.remove();
                }, 1500);
            });
        });