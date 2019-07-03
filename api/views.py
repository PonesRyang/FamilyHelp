from django.db.transaction import atomic
from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_framework.generics import ListAPIView
from api.models import Users, Article, Comment, Complain, OrderComplain, Orders, StarArticle
from api.serializers import ArticleSerializer, OrderDetailSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from api.filters import OrderFilterSet


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


class OrderViewsSet(ModelViewSet):
	queryset = Orders.objects.all()
	serializer_class = OrderDetailSerializer
	filter_backends = (OrderingFilter,)
	ordering = ('-order_createtime',)

	def get_queryset(self):
		u_id = self.request.data['user']
		user = Users.objects.filter(u_id=u_id).first()
		self.queryset = Orders.objects.filter(users=u_id).all()
		return self.queryset


@api_view(['POST'])
def comments(request):
	try:
		user = request.data.get('user', '')
		order = request.data.get('order_id', '')
		content_star = request.data.get('content_star', '')
		content = request.data.get('content', '')
		comment = Comment()
		comment.user_id = user
		comment.order_id = order
		comment.content = content
		comment.content_star = content_star
		comment.save()
		data = {'code': 200, 'mes': '评价成功'}
	except:
		data = {'code': 300, 'mes': '评价失败,请稍后再试'}
	return JsonResponse(data)


@api_view(['POST'])
def complain(request):
	try:
		user1 = request.data.get('user', None)
		order_number = request.data.get('order_number', None)
		complain_content = request.data.get('complain_content', None)
		order = Orders.objects.filter(order_number=order_number).first()
		users = order.users_set.all()
		user2 = ''
		for user in users:
			if user.u_id != int(user1):
				user2 = user
		complain = Complain()
		if user2:
			complain.u = user2
			complain.complain_content = complain_content
			complain.save()
			ordercomplain = OrderComplain()
			ordercomplain.complain = complain
			ordercomplain.order = order
			ordercomplain.save()
		data = {'code': 200, 'mes': '投诉成功'}
	except:
		data = {'code': 300, 'mes': '投诉失败,请稍后再试'}
	return JsonResponse(data)


@api_view(['POST'])
def add_star_article(request):
	# try:
	with atomic():
		new_star = StarArticle()
		new_star.article = Article.objects.filter(ar_id=request.data.get('article_id')).first()
		new_star.star = request.data.get('article_star')
		# new_star.user = request.session['user']
		new_star.user = Users.objects.filter(u_id=1).first()
		new_star.save()
		data = {'code':200,'mes':'评价成功'}
	# except:
	# 	data = {'code':400,'mes':'评价失败，请重试'}
	return JsonResponse(data)