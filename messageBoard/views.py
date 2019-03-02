from django.shortcuts import render,HttpResponse
from django.core import serializers
from messageBoard import models
from django.http import JsonResponse
import datetime
import math,re

# Create your views here.
one_page=5      #一页数据的条数

#留言板页：
def render_message_board(request):
    return render(request,"messageBoard.html")

#返回已有的留言：
def sendMessage(request,type):
    global one_page
    try:
        curPage=int(request.POST.get('page',1))
    except ValueError:
        curPage=1

    if type=="public":
        total=models.publicMessage.objects.count()
        #利用分片懒惰查询，高效率！
        if total<curPage*one_page:  #最后一页不足
            num = total - (curPage - 1) * one_page
            messages = models.publicMessage.objects.all()[0:total - (curPage - 1) * one_page]
        else:                       #正常分页
            num = one_page
            messages=models.publicMessage.objects.all()[total-curPage*one_page:total-(curPage-1)*one_page]


    elif type=="private":
        user=request.POST.get('username')
        queryset=models.privateMessage.objects.filter(username=user)
        total=queryset.count()
        if total<curPage*one_page:  #最后一页不足
            num=total - (curPage - 1) * one_page
            messages = queryset[0:total - (curPage - 1) * one_page]
        else:                       #正常分页
            num=one_page
            messages=queryset[total-curPage*one_page:total-(curPage-1)*one_page]
    else:return HttpResponse("查询错误！")

    dayReg="^\d{4}-\d{2}-\d{2}"
    timeReg="(\d{2}:\d{2}):\d{2}"
    timeList=[]
    reply_list=[]
    for i in range(num):
        now=datetime.datetime.now()
        time_str=messages[i].time.strftime("%Y-%m-%d %H:%M:%S")
        if now.day==messages[i].time.day:
            time=re.search(timeReg,time_str).group(1)
            timeList.append(time)
        elif now.day-messages[i].time.day==1:
            time = re.search(timeReg, time_str).group(1)
            timeList.append('昨天 '+time)
        else:
            day = re.search(dayReg, time_str).group()
            timeList.append(day)
        if type=="public":
            if messages[i].reply!=-1:
                reply_info=models.publicMessage.objects.get(id=messages[i].reply)
                reply_list.append([reply_info.username,reply_info.content])
            else:
                reply_list.append(-1)

    page_num=math.ceil(total/one_page)#计算页数，向上取整
    json_data = serializers.serialize("json", messages, ensure_ascii=False)
    if type=="public":
        return JsonResponse({"message_list": json_data, "page_num": page_num, "time_list": timeList,"reply_list":reply_list})
    else:
        return JsonResponse({"message_list":json_data,"page_num":page_num,"time_list":timeList})

#接收留言：
def getMessage(request,type):
    if request.method=='POST':
        try:
            username=request.POST.get("username")
            message=request.POST.get("message")
            reply=request.POST.get("reply")
            message=re.sub("\s+"," ",message)
            if type == 'public':
                new_message=models.publicMessage.objects.create()
            else:
                new_message = models.privateMessage.objects.create()
            if username!='':
                new_message.username=username
            new_message.content=message
            new_message.reply=reply
            new_message.save()
            return JsonResponse({"hhh":"ok"})
        except:
            return HttpResponse("留言出现错误！")

#删除留言：
def delMessage(request):
    global one_page
    type=request.POST.get("type")
    pk=request.POST.get("pk")
    if type=="public":
        models.publicMessage.objects.filter(id=pk).delete()
        total=models.publicMessage.objects.count()
    else:
        user=models.privateMessage.objects.filter(id=pk)[0].username
        models.privateMessage.objects.filter(id=pk).delete()
        total=models.privateMessage.objects.filter(username=user).count()

    page_num = math.ceil(total / one_page)  # 计算页数，向上取整
    return JsonResponse({"page_num":page_num})