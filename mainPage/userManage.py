from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.core.mail import send_mail
from mainPage import models
from django.conf import settings
import uuid,hashlib

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
        request.session["is_login"]=True
        request.session["user_id"]=new_user.id
        request.session["user_name"]=new_user.username
        #发送邮件：
        random_str=get_random_str()

        url = "www.cguo16.com/activate/?token=" + random_str
        send_mail(subject="cguo16：账号激活",
                  message=username+" 您好，请点击下面的链接，激活您在cguo16网站的账号\n\n"+url,
                  recipient_list=[email],
                  from_email='cguo16 <743535469@qq.com>'
                  )
        new_user.uuid=random_str
        new_user.save()
        return render(request,"requestForActivate.html",{"email":email})

#生成激活邮件用到的随机id：
def get_random_str():
    uuid_val = uuid.uuid4()
    uuid_str = str(uuid_val).encode("utf-8")
    md5 = hashlib.md5()
    md5.update(uuid_str)
    return md5.hexdigest()

#激活账号：
def activate(request):
    token=request.GET["token"]
    try:
        user=models.User.objects.get(uuid=token)
        email=user.mail
        user.isActive=True
        user.save()
        return render(request, "activated.html", {"username":user.username})
    except:
        return HttpResponse("激活过程出现错误！")

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

#返回用户信息：
def sendUserInfo(request):
    if(request.method=="POST"):
        try:
            username=request.POST.get("username")
            user=models.User.objects.get(username=username)
            return JsonResponse({"email":user.mail,"isActive":user.isActive})
        except:
            return HttpResponse("用户信息错误！")
