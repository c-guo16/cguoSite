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
from mainPage import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.render_index),
    path('fileTransfer',views.render_file_transfer),
    path('signUp',views.render_sign_up),
    path('signIn',views.render_sign_in),
    path('userAgreement',views.render_user_agreement),
    path('postSignUp',views.handle_sign_up_form),
    path('postSignIn',views.handle_sign_in_form),
    path('logOut',views.logout),
    path('postDuplicateCheck',views.check_username_email)
]

urlpatterns += staticfiles_urlpatterns()
