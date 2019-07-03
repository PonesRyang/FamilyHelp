from django.http import HttpRequest
from django.shortcuts import render, redirect


def login_authentication_middleware(func):
    def wrapper(request, *args, **kwargs):
        try:
            un_authentication_list = ['/login/','/logout']
            if request.session.get('user'):
                resp = func(request, *args, **kwargs)
            else:
                resp = redirect('/login/')
            if request.path in un_authentication_list:
                resp = func(request, *args, **kwargs)
        except Exception:
            # 记录异常日志
            resp = redirect('/login/')
        return resp
    return wrapper