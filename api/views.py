from django.contrib.auth.models import User
from django.core.cache import caches
from django.db.transaction import atomic
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.decorators import api_view

from api.forms_helper import LoginForm
from api.models import Users
from captcha import Captcha
from utils import random_captcha_text, random_mobile_code, send_code_by_sms


def get_captcha(request):
	""" 验证码 """
	captcha_text = random_captcha_text()
	request.session['captcha'] = captcha_text
	image_data = Captcha.instance().generate(captcha_text)
	return HttpResponse(image_data, content_type='image/png')

def send_mobile_code(request, tel):
    """发送短信验证码"""
    code = random_mobile_code()
    if tel in caches['mobile']:
        data = {'code': 403, 'message': '请不要在120秒内重复发送'}
    else:
        result = send_code_by_sms(tel, code)
        if result['error'] == 0:
            # 将手机验证码保存到缓存中
            caches['mobile'].set(tel, code, timeout=120)
            data = {'code': 200, 'message': '短信验证码已发送'}
        else:
            data = {'code': 404, 'message': '短信验证码服务暂时无法使用'}
    return JsonResponse(data)



# @api_view(['GET','POST'])
# def register(request):
# 	if request.method=='GET':
# 		pass
# 	if request.method=='POST':
# 		pass



@api_view(['GET','POST'])
def login(request):
	if request.method=='GET':
		return render(request, 'login.html')
	if request.method=='POST':
		form  = LoginForm(request.POST)
		if form.is_valid():
			captcha_from_user = form.cleaned_data['captcha']
			captcha_from_sess = request.session.get('captcha', '')
			if captcha_from_sess.lower() != captcha_from_user.lower():
				hint = '请输入正确的图形验证码'
			else:
				tel = form.cleaned_data['tel']
				# user = User.objects.filter(tel=tel).first()
				# if tel:
				# request.session['user'] = user
				return HttpResponse('跳转首页成功')
				# else:
				# 	hint = '用户名或密码错误'
		else:
			hint = '请输入有效的登录信息'
	return render(request, 'login.html', {'hint': hint})






@api_view(['PUT'])
def change_information(request):
	u_tel = request.data.get('u_tel')
	u_birthday = request.data.get('u_birthday')
	if u_tel or u_birthday:
		# request.session['user'] = Users.objects.create(**{'u_tel':u_tel,'u_birthday':'1996-07-26'})
		with atomic():
			user = request.session['user']
			user.u_tel = u_tel
			user.u_birthday = u_birthday
			user.save()
		# request.session.clear()
		data = {'code': 200, 'mes': '用户信息修改成功'}
	else:
		data = {'code': 300, 'mes': '未添加需要修改的信息'}
	return JsonResponse(data=data)


@api_view(['DELETE'])
def logout(request):
	request.session.clear()
	return JsonResponse(data={'code': 200, 'back_url': 'index/'})


@api_view(['PUT'])
def check_card_id(request):
	card_id = request.data.get('card_id')
	u_relname = request.data.get('u_relname')
	# 调用第三方接口，验证用户名称与身份证号是否一致
	if True:  # 如果验证结果返回成功
		with atomic():
			user = request.session['user']
			user.card_id = card_id
			user.u_relname = u_relname
			user.save()
		data = {'code': 200, 'mes': '实名认证成功'}
	else:  # 如果返回失败
		data = {'code': 400, 'mes': '认证失败'}
	return JsonResponse(data)