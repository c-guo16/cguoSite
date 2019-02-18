from django.shortcuts import render

# Create your views here.

#留言板页：
def render_message_board(request):
    return render(request,"messageBoard.html")
