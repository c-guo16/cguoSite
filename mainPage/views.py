from django.shortcuts import render,redirect
from django.http import JsonResponse
from mainPage import models

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

#检查注册时填写的用户名和邮箱：
def check_username_email(request):
    if request.method == "POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        if username:
            same_name_user = models.User.objects.filter(username=username)
            if same_name_user:  #用户名已存在
                return JsonResponse({"message":"用户名已存在！"})
        if email:
            same_email=models.User.objects.filter(mail=email)
            if same_email:      #邮箱被占用
                return JsonResponse({"message": "邮箱已被占用！"})
        return JsonResponse({"message": "ok"})

#注册表单处理：
def handle_sign_up_form(request):
    if request.method=="POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        if username:
            same_name_user = models.User.objects.filter(username=username)
            if same_name_user:  # 用户名已存在
                return redirect('/')
        if email:
            same_email = models.User.objects.filter(mail=email)
            if same_email:  # 邮箱被占用
                return redirect('/')
        new_user=models.User.objects.create()
        new_user.username=request.POST.get("username")
        new_user.password=request.POST.get("password")
        new_user.mail=request.POST.get("email")
        new_user.isActive=False
        new_user.save()
        return render(request,"requestForActivate.html",{"email":email})

#登录页：
def render_sign_in(request):
    message=request.session.get('message',None)
    if message:
        del request.session["message"]
        return render(request,"signIn.html",{"message":message})
    else:
        return render(request, "signIn.html")

#登录表单处理：
def handle_sign_in_form(request):
    if request.session.get('is_login', None):
        return redirect('/')
    message=""
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        try:
            user = models.User.objects.get(username=username)
            if user.password==password:
                request.session['is_login'] = True      #保存登录状态
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return redirect("/")
            else:
                message="密码错误！"
        except :
            message="用户不存在！"
    request.session['message'] = message
    return redirect( '/signIn')

#登出：
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    request.session.flush()
    return redirect("/")

#用户协议页：
def render_user_agreement(request):
    return render(request,"userAgreement.html")