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
def index(request):
    global visit_times
    visit_times = visit_times + 1  #访问次数增加
    print(get_ip(request))          #打印ip
    return render(request,'index.html',{"v_times":visit_times})