"""cguoSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainPage import views as mpviews
from messageBoard import views as mbviews
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    #导航栏按键：
    path('',mpviews.render_index),
    path('fileTransfer',mpviews.render_file_transfer),
    path('messageBoard',mbviews.render_message_board),

    #用户管理功能：
    path('signUp',mpviews.render_sign_up),
    path('signIn',mpviews.render_sign_in),
    path('userAgreement',mpviews.render_user_agreement),
    path('postSignUp',mpviews.handle_sign_up_form),
    path('postSignIn',mpviews.handle_sign_in_form),
    path('logOut',mpviews.logout),
    path('postDuplicateCheck',mpviews.check_username_email),
    path('activate/',mpviews.activate),
    path('userInfo',mpviews.render_user_info),
    path('postUserInfo',mpviews.sendUserInfo),

    #留言板功能：
    path('getPublicMessage',mbviews.sendPublicMessage),
    path('getPrivateMessage',mbviews.sendPrivateMessage),
    path('postPublicMessage',mbviews.getPublicMessage),
    path('postPrivateMessage',mbviews.getPrivateMessage)
]

urlpatterns += staticfiles_urlpatterns()
