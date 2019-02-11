#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Charles Guo'
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render

def send_activate_mail(request,to, subject, template, **kwargs):
    html = render(request, template+'.html',{'token':kwargs['token'],'username':kwargs['username']})
    text = render(request, template+'.txt', {'token':kwargs['token'],'username':kwargs['username']})

    msg = EmailMultiAlternatives(subject, text.content.decode('utf-8'), '18570329382@163.com', ['454995446@qq.com'])
    msg.attach_alternative(html.content.decode('utf-8'), "text/html")

    msg.send()

