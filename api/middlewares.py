import re

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect


def login_authentication_middleware(func):
	def wrapper(request, *args, **kwargs):
		try:
			un_authentication_list = ['/api/login/', '/api/captcha/']
			pattern = r'/api/mobile/1[0-9]{10}/'
			if re.search(pattern,request.path):
				resp = func(request, *args, **kwargs)
			elif request.session.get('user'):
				resp = func(request, *args, **kwargs)
			elif request.path in un_authentication_list:
				resp = func(request, *args, **kwargs)
			else:
				return JsonResponse(data={'code': 300, 'mes': '请登陆后再试'})
		except Exception:
			# 记录异常日志
			resp = redirect('/login/')
		return resp

	return wrapper
