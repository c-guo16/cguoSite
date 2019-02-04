from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.

#访问次数：
visit_times=0

def index(request):
    global visit_times
    visit_times = visit_times + 1
    return render(request,'index.html',{"v_times":visit_times})