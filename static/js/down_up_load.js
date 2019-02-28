/**
 * Created by guocheng on 2019/2/26.
 */

function download() {
    var files=tree.getSelectedNodes();
    if(!files.length)return;
    var id=1;
    var $form = $("<form method='post'></form>");
    $form.attr("action","/downloadFiles");
    $form.append($("<input></input>").attr("type", "hidden").attr("name", "filenum").attr("value", files.length));
    for(var i=0;i<files.length;i++){
        $form.append($("<input></input>").attr("type", "hidden").attr("name", i).attr("value", files[i].path));
    }
    $form.append($("<input></input>").attr("type", "hidden").attr("name", "csrfmiddlewaretoken").attr("value", vars.csrf_token));
    $form.appendTo('body').submit().remove();
}