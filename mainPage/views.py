from mainPage.userManage import *

# Create your views here.

#访问次数：
visit_times=0

#获取用户ip：
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]#所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')#这里获得代理ip
    return ip

#首页：
def render_index(request):
    global visit_times
    visit_times = visit_times + 1  #访问次数增加
    return render(request,'index.html',{"v_times":visit_times,"v_ip":get_ip(request),"current_page":"main"})

#文件服务页：
def render_file_transfer(request):
    return render(request,"fileTransfer.html",{"current_page":"fileTransfer"})

#注册页：
def render_sign_up(request):
    return render(request,"signUp.html")

#登录页：
def render_sign_in(request):
    message=request.session.get('message',None)
    if message:
        del request.session["message"]
        return render(request,"signIn.html",{"message":message})
    else:
        return render(request, "signIn.html")

#用户协议页：
def render_user_agreement(request):
    return render(request,"userAgreement.html")

#查看用户状态页：
def render_user_info(request):
    return render(request,"userInfo.html")
