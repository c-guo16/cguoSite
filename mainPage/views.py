from django.shortcuts import render
from django.shortcuts import HttpResponse

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
    print(get_ip(request))          #打印ip
    return render(request,'index.html',{"v_times":visit_times,"v_ip":get_ip(request),"current_page":"main"})

#文件服务页：
def render_file_transfer(request):
    return render(request,"fileTransfer.html",{"current_page":"fileTransfer"})

#注册页：
def render_sign_up(request):
    return render(request,"signUp.html")

#注册表单处理：
def handle_sign_up_form(request):
    if request.method=="POST":
        username=request.POST.get("username")
        print(username)

#登录页：
def render_sign_in(request):
    return render(request,"signIn.html")

#登录表单处理：
def handle_sign_in_form(request):
    if request.method=="POST":
        username=request.POST.get("username","")
        print(username)

#用户协议页：
def render_user_agreement(request):
    return render(request,"userAgreement.html")