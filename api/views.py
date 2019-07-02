from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

from api.models import Users, Article
from api.serializers import ArticleSerializer


@api_view(['POST'])
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


@api_view(['POST'])
def logout(request):
	request.session.clear()
	return JsonResponse(data={'code': 200, 'back_url': '   /'})


@api_view(['POST'])
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


class ArticleAPIView(ListAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer
	pagination_class = None