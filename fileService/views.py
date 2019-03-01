from django.shortcuts import render,HttpResponse
from django.http import JsonResponse,FileResponse,StreamingHttpResponse
from django.core import serializers
from django.utils.http import urlquote
from mainPage import models
from wsgiref.util import FileWrapper
import os,zipfile,tempfile,shutil

# Create your views here.
FILE_ROOT_PATH= '../files'
TEMPFILE_ROOT_PATH='../tempfiles'
icon_dict={
    ".txt":"txt",
    ".mp3":"music",
    ".wav":"music",
    ".ape":"music",
    ".flac":"music",
    ".m4a":"music",
    ".mp4":"video",
    ".avi":"video",
    ".mov":"video",
    ".mpeg":"video",
    ".mpg":"video",
    ".rar":"rar",
    ".zip":"rar",
    ".7z":"rar",
    ".doc":"word",
    ".docx":"word",
    ".ppt":"ppt",
    ".pptx":"ppt",
    ".xls":"excel",
    ".csv":"excel",
    ".pdf":"pdf",
    ".exe":"exe",
    ".jpg":"image",
    ".png":"image",
    ".jpeg":"image",
    ".gif":"image",
    ".bmp":"image"
}

#判断当前用户是否激活：
def activateCheck(request):
    try:
        user=request.POST.get("username")
        isActive=models.User.objects.filter(username=user)[0].isActive
        return JsonResponse({"isActive":isActive})
    except:
        return HttpResponse("查询错误!")

#递归遍历指定目录：
def getAlldirInDiGui(path,nodelist,plist,counter):
    global icon_dict
    filesList = os.listdir(path)
    for fileName in filesList:
        counter[0]+=1
        fileAbpath = os.path.join(path, fileName)
        nodelist.append({"id": counter[0], "pId": plist[path], "name": fileName,"path":fileAbpath})
        plist[fileAbpath]=counter[0]
        if os.path.isdir(fileAbpath):
            nodelist[-1]["isParent"]=True
            getAlldirInDiGui(fileAbpath,nodelist,plist,counter)
        else:
            suffix=os.path.splitext(fileName)[-1].lower()
            if suffix in icon_dict:
                nodelist[-1]["iconSkin"] =icon_dict[suffix]


#发送可下载文件列表：
def sendFileList(request):
    global FILE_ROOT_PATH
    nodelist=[{"id":1,"pId":0,"name":"files","path":FILE_ROOT_PATH,"isParent":True}]
    parent_list={FILE_ROOT_PATH:1}
    counter=[1]
    getAlldirInDiGui(FILE_ROOT_PATH, nodelist, parent_list, counter)
    return JsonResponse({"data":nodelist})


#下载指定文件：
def sendFiles(request):
    global FILE_ROOT_PATH
    try:
        filenum=int(request.POST.get('filenum'))
        if filenum==1 and not os.path.isdir(request.POST.get("0")):  #发送单个文件
            file = open(request.POST.get("0"), 'rb')
            response = FileResponse(file)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="%s"' % (urlquote(os.path.basename(request.POST.get("0"))))
            return response
        else:   #发送单个文件夹
            filepath=request.POST.get('0')
            shutil.make_archive(TEMPFILE_ROOT_PATH+os.path.basename(filepath), 'zip',root_dir=filepath)
            file = open(TEMPFILE_ROOT_PATH+os.path.basename(filepath)+'.zip', 'rb')
            response = FileResponse(file, content_type='application/zip')
            response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(os.path.basename(filepath)+'.zip'))
            return response
    except:
        return HttpResponse("下载出现错误！")

