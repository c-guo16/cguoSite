/**
 * Created by guocheng on 2019/2/23.
 */

//在页面中央显示通知：
function display_note_dynamic() {
    $('.tabs .note_dynamic').css("display","block");
    $('.tabs .note_dynamic').fadeOut(1500);
}

//提交留言：
function postMessage(type) {
    if(type==='public') {        //公共留言
        $.ajax({
            type: "POST",
            url: "/postPublicMessage",
            data: {
                "username":vars.user_name,
                "message": $('div.active textarea').val(),
                csrfmiddlewaretoken: vars.csrf_token
            },
            success: function (result) {
                $('div.active textarea').val('');
                $('div.active .button').attr("disabled",true);
                $('div.active .limit').text('0/140');
                $('.note_dynamic span').text("✔ 留言成功");
                display_note_dynamic();
                getMessage("public",1);
            }
        });
    }
    else if(type==='private'){  //私信
        $.ajax({
            type:"POST",
            url:"/postPrivateMessage",
            data:{"username":vars.user_name,
                    "message":$('div.active textarea').val(),
                     csrfmiddlewaretoken: vars.csrf_token},
            success:function(result) {
                $('div.active textarea').val('');
                $('div.active .button').attr("disabled",true);
                $('div.active .limit').text('0/140');
                $('.note_dynamic span').text("✔ 留言成功");
                display_note_dynamic();
                if(vars.user_name){
                    getMessage("private",1);    //获取当前用户的留言
                }
            }
        });
    }
}

//换页：
function change_page(result,page,type) {
    var page_str='';
    var page_num=result.page_num;
    var current_page=page;
    page_str+='<button type="button" class="page_button toleft" onclick="getMessage(\''+type+'\','+(current_page-1)+')"><</button>';
    if(current_page>4){    //左省略号
        page_str+='<button type="button" class="page_button" onclick="getMessage(\''+type+'\',1)">1</button>';
        page_str+='<span>...</span>';
        page_str+='<button type="button" class="page_button" onclick="getMessage(\''+type+'\','+(current_page-2)+')">'+(current_page-2)+'</button>';
        page_str+='<button type="button" class="page_button" onclick="getMessage(\''+type+'\','+(current_page-1)+')">'+(current_page-1)+'</button>';
    }
    else{   //左无省略号
        for(var j=1;j<current_page;j++){
            page_str+='<button type="button" class="page_button" onclick="getMessage(\''+type+'\','+j+')">'+j+'</button>';
        }
    }
    page_str+='<button type="button" class="page_button active" onclick="getMessage(\''+type+'\','+current_page+')">'+current_page+'</button>';
    if(current_page<page_num-3){    //右省略号
        page_str+='<button type="button" class="page_button" onclick="getMessage(\''+type+'\','+(current_page+1)+')">'+(current_page+1)+'</button>';
        page_str+='<button type="button" class="page_button" onclick="getMessage(\''+type+'\','+(current_page+2)+')">'+(current_page+2)+'</button>';
        page_str+='<span>...</span>';
        page_str+='<button type="button" class="page_button" onclick="getMessage(\''+type+'\','+page_num+')">'+page_num+'</button>';
    }
    else{   //右无省略号
        for(var r=current_page+1;r<=page_num;r++){
            page_str+='<button type="button" class="page_button" onclick="getMessage(\''+type+'\','+r+')">'+r+'</button>';
        }
    }
    page_str+='<button type="button" class="page_button toright" onclick="getMessage(\''+type+'\','+(current_page+1)+')">></button>';
    $('div#'+type+' .changePage_area').html(page_str);
    $('div#'+type+' .page_button').css({
        "width":"1.875rem",
        "height":"1.875rem",
        "margin-left":"0.1875rem",
        "margin-right":"0.1875rem",
        "background":"#f8f8f8",
        "border":"0",
        "font-size":"0.9375rem",
        "cursor":"pointer",
        "color":"#797979"
    });
    $('div#'+type+' .page_button').hover(function () {
        $(this).css({
            "background":"#f0f0f0",
            "border":"0.0625rem solid #6b6b6b",
            "color":"black",
            "font-weight":"bold"
        });
    },function () {
        $(this).css({
            "background":"#f8f8f8",
            "border":"0",
            "color":"#797979",
            "font-weight":"normal"
        });
        if($(this).hasClass('toleft')||$(this).hasClass('toright')){
            $(this).css({
                "border":"0.0625rem solid #d3d3d3",
                "font-weight":"bold"
            });
        }
        $('div#'+type+' .page_button.active').css({
            "color":"#4285f4",
            "text-decoration":"underline"
        });
    });
    $('div#'+type+' .page_button.active').css({
        "color":"#4285f4",
        "text-decoration":"underline"
    });
    $('div#'+type+' .toleft').css({
        "border":"0.0625rem solid #d3d3d3",
        "font-weight":"bold",
        "font-size":"1.125rem"
    });
    $('div#'+type+' .toright').css({
        "border":"0.0625rem solid #d3d3d3",
        "font-weight":"bold",
        "font-size":"1.125rem"
    });
    $('div#'+type+' .toleft').attr("disabled",false);
    $('div#'+type+' .toright').attr("disabled",false);
    if(current_page===1){
        $('div#'+type+' .toleft').attr("disabled",true);
        $('div#'+type+' .toleft').css({
            "color":"#d3d3d3",
            "cursor":"default"
        });
    }
    if(current_page>=page_num){
        $('div#'+type+' .toright').attr("disabled",true);
        $('div#'+type+' .toright').css({
            "color":"#d3d3d3",
            "cursor":"default"
        });
    }
}

//展示评论：
function display_messages(result,page,type) {
    var messages=JSON.parse(result.message_list);
    var str='';
    if(messages.length===0){
        str += '<hr class="input_hr">';
        str +='<p style="text-align:center">当前还没有留言。</p>';
        $('div#private .display_area').html(str);
        $('div#private .display_area .input_hr').css({
            "align-items":"center",
            "width":"46.25rem",
            "color": "#d3d3d3",
            "margin": "0 auto 0.5rem auto"
        });
    }
    for(var i=messages.length-1;i>-1;i--) { //拼接展示评论的html
        str += '<hr class="input_hr">';
        str += '<div class="single_message">';
        str += '<p class="message_word"><span style="color:blue">' + messages[i]["fields"]["username"] + "</span>：" + messages[i]["fields"]["content"] + '</p>';
        str += '<p style="color:#646464;font-size:0.5rem">' + result.time_list[i];
        //自己的评论可以删除：
        if(messages[i]["fields"]["username"]!=='游客'&&messages[i]["fields"]["username"]===vars.user_name){
            str += '<span id=\''+messages[i]["pk"]+'\' class="delete" onclick="deleteMessage('+messages[i]["pk"]+',\''+type+'\')">删除</span>'
        }
        str += '</p></div>';
    }
    $('div#'+type+' .display_area').html(str);
    $('div#'+type+' .delete').css({
        "float":"right",
        "cursor":"pointer"
    });
    change_page(result,page,type);
    $('div#'+type+' .display_area .input_hr').css({
        "align-items":"center",
        "width":"46.25rem",
        "color": "#d3d3d3",
        "margin": "0 auto 0.5rem auto"
    });
    $('div#'+type+' .display_area .single_message').css({
        "width":"80%",
        "margin": "0 auto 0.5rem auto"
    });
    $('div#'+type+' .display_area .message_word').css({
        "word-break":"normal",
        "white-space":"pre-line",
        "word-wrapL":"break-word"
    });
}

//获取数据库中的留言：
function getMessage(type,page) {
    if(type==='public') {        //公共留言
        $.ajax({
            type: "POST",
            url: "/getPublicMessage",
            data: {
                "page":page,
                csrfmiddlewaretoken: vars.csrf_token
            },
            success: function (result) {
                vars.current_page=page;
                display_messages(result,page,type);
            }
        });
    }
    else if(type==='private'){  //私信
        $.ajax({
            type:"POST",
            url:"/getPrivateMessage",
            data:{
                "page":page,
                "username":vars.user_name,
                csrfmiddlewaretoken: vars.csrf_token
            },
            success:function(result) {
                vars.current_page=page;
                display_messages(result,page,type);
            }
        });
    }
}

//删除评论：
function deleteMessage(pk,type) {
    $('.delete_mask').css({
        "display":"block",
        "height":$(document).height(),
        "width":$(document).width()
    });
    $('.tabs .delete_window').css("display","block");
    $('.tabs .delete_window .confirm').on("click",function() {
        $('.tabs .delete_window').css("display","none");
        $('.delete_mask').css("display","none");
        $('.tabs .delete_window .confirm').off("click");
        deleteMessage_confirm(pk, type);
    });
}

//确定删除：
function deleteMessage_confirm(pk,type) {
    $.ajax({
        type:"POST",
        url:"/postDeleteMessage",
        data:{
            "type":type,
            "pk":pk,
            "current_page":vars.current_page,
            csrfmiddlewaretoken: vars.csrf_token
        },
        success:function (result) {
            if(result.page_num!==0) {
                if (vars.current_page > result.page_num) {
                    vars.current_page = result.page_num;
                }
                getMessage(type, vars.current_page);
            }else{
                str='';
                str += '<hr class="input_hr">';
                str +='<p style="text-align:center">当前还没有留言。</p>';
                $('div#private .display_area').html(str);
                $('div#private .display_area .input_hr').css({
                    "align-items":"center",
                    "width":"46.25rem",
                    "color": "#d3d3d3",
                    "margin": "0 auto 0.5rem auto"
                });
            }
            $('.note_dynamic span').text("✔ 删除成功");
            display_note_dynamic();
        },
        error:function (result) {

        }
    })
}