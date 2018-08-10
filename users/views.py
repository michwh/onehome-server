from django.shortcuts import render, redirect

# def register(request):
#     # 只有当请求为 POST 时，才表示用户提交了注册信息
#     if request.method == 'POST':
#         # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
#         # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
#         # 用这些数据实例化一个用户注册表单
#         form = RegisterForm(request.POST)
#
#         # 验证数据的合法性
#         if form.is_valid():
#             # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
#             form.save()
#
#             # 注册成功，跳转回首页
#             return redirect('/')
#     else:
#         # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
#         form = RegisterForm()
#
#     # 渲染模板
#     # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
#     # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
#     return render(request, 'users/register.html', context={'form': form})

from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from users.models import User

import pdb

def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单信息
            username = uf.cleaned_data['username']
            # pdb.set_trace()
            # try:
            filterResult = User.objects.filter(username=username)
            if len(filterResult) > 0:
                return render_to_response('index.html', {"errors": "用户名已存在"})
            else:
                password1 = uf.cleaned_data['password1']
                password2 = uf.cleaned_data['password2']
                errors = []
                if password2 != password1:
                    errors.append("两次输入的密码不一致!")
                    return render_to_response('index.html', {'errors': errors})
                    # return HttpResponse('两次输入的密码不一致!,请重新输入密码')
                password = password2
                email = uf.cleaned_data['email']
                # 将表单写入数据库
                user = User.objects.create(username=username, password=password1)
                # user = User(username=username,password=password,email=email)
                user.save()
                pdb.set_trace()
                # 返回注册成功页面
                return render_to_response('index.html', {'username': username, 'operation': "注册"})
    else:
        uf = UserForm()
    return render_to_response('index.html', {'uf': uf})


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')