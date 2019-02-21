from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core import serializers
from messageBoard import models
from django.http import JsonResponse
import math,re

# Create your views here.

#留言板页：
def render_message_board(request):
    return render(request,"messageBoard.html")

#返回已有的公共留言：
def sendPublicMessage(request):
    one_page=5      #一页数据的条数
    try:
        curPage=int(request.POST.get('page',1))
        allPage=int(request.POST.get('allPage',1))
    except ValueError:
        curPage=1
        allPage=1

    total=models.publicMessage.objects.count()
    #利用分片懒惰查询，高效率！
    if total<curPage*one_page:  #最后一页不足
        messages = models.publicMessage.objects.all()[0:total - (curPage - 1) * one_page]
    else:                       #正常分页
        messages=models.publicMessage.objects.all()[total-curPage*one_page:total-(curPage-1)*one_page]

    for i in range(one_page):

    page_num=math.ceil(total/one_page)#计算页数，向上取整
    json_data = serializers.serialize("json", messages, ensure_ascii=False)
    return JsonResponse({"message_list":json_data,"page_num":page_num})

#返回已有的私信：
def sendPrivateMessage(request):
    pass

#接收公共留言：
def getPublicMessage(request):
    if request.method=='POST':
        username=request.POST.get("username")
        message=request.POST.get("message")
        message=re.sub("\s+"," ",message)
        new_message=models.publicMessage.objects.create()
        if username!='0':
            new_message.username=username
        new_message.content=message
        new_message.save()

    return JsonResponse({"hhh":"ok"})

#获取私信：
def getPrivateMessage(request):
    pass