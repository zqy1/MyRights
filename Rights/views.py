# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from Rights.models import Student,Arcitle


def index(request):
    # user = request.user    OneToOne
    user = request.user if request.user.is_authenticated() else None

    content = {
        'active_menu': 'index',
        'user': user,
    }
    return render(request, 'Rights/index.html', content)


def signup(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    state = None
    if request.method == 'POST':
        mobilephone = request.POST.get('mobilephone','')
        checkcode = request.POST.get('checkcode','')

        password = request.POST.get('password','')
        repeat_password = request.POST.get('repeat_password','')
        if len(mobilephone) != 11:
            state = 'phone_error'
        elif password == '' or repeat_password == '':
            state = 'empty'
        elif password <= 5:
            state = 'too_short'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username,password=password,)
                new_user.save()
                new_my_user = Student(user=new_user,mobile=mobilephone)
                new_my_user.save()
                state = 'success'
    content = {
        'state':state,
        'user':None,
    }
    return render(request,'Rights/signup.html',content)

def login(request):
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect(reverse('index'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            state='not_exist_or_password_error'
    content = {
        'state': state,
        'user': None,

    }
    return render(request,'Rights/login.html',content)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def complain(request):
    user = request.user if request.user.is_authenticated() else None

    if request.method == 'POST':
        my_arcitle = Arcitle(
            title=request.POST.get('title',''),
            body=request.POST.get('body',''),
            # ForeignKey 的使用
            author=User.objects.get(id=request.user.id),
        )
        my_arcitle.save()

    content = {
        'user': user,
    }
    return render(request,'Rights/complain.html', content)