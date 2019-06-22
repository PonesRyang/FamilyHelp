import uuid
from time import timezone

from rest_framework.response import Response
from django.shortcuts import render
from hashlib import md5
from django.db.transaction import atomic
from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_framework.generics import ListAPIView,RetrieveAPIView
from api.models import Users, Article, Comment, Complain, OrderComplain, Orders, Roles, OrderType, District
from api.serializers import ArticleSerializer, OrderDetailSerializer,StarStaffSerializer, OrdersTypeSerializer, DistrictSimpleSerializer, \
    DistrictDetailSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from api.filters import OrderFilterSet, StarStaffFilterSet
from api.forms import UserInfoForm


class DistrictViewSet(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSimpleSerializer


@api_view(['POST'])
def SubmitList(request):
    order_addr = request.data.get('order_addr')
    order_plantime = request.data.get('order_plantime')
    district = request.data.get('district')
    district1 = District.objects.get(name=district)
    user = request.session.get('user')
    if order_addr and order_plantime:
        current_time = timezone.now()
        order =Orders()
        order.order_addr = order_addr
        order.order_plantime = order_plantime
        order.order_createtime = current_time
        order.district = district1
        order.u = user
        order.order_status = 2
        order.order_number = uuid.uuid4().hex
        order.save()
        data={
            'code':200, 'message':'订单已生成'
        }
    else:
        data={
            'code':300, 'message':'订单地址不能为空'
        }
    return Response(data)


class StarStaffView(ListAPIView):
    """查看星级家政人员"""
    queryset = Users.objects.all()
    serializer_class = StarStaffSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = StarStaffFilterSet

    def get_queryset(self):
        role = Roles.objects.filter(r_code=1)
        queryset = Users.objects.filter(role=role)
        return queryset


class OrdersTypeViewSet(ModelViewSet):
    queryset = OrderType.objects.all()
    serializer_class = OrdersTypeSerializer
    pagination_class = None


# 获取所有省级行政单位 - GET /api/districts/
class ProvinceView(ListAPIView):
    """查看各省的id和名称"""
    # only defer 优化SQL查询
    queryset = District.objects.filter(parent__isnull=True).only('distid',)
    # queryset = District.objects.filter(parent__isnull=True).defer('ishot','intro')
    serializer_class = DistrictSimpleSerializer
    pagination_class = None


# 获取指定行政单位详情及其管辖的行政单位 - GET /api/districts/{行政单位编号}
class DistrictView(RetrieveAPIView):
    """查看各省的id,名称,介绍及其下各市区的id和名称"""
    queryset = District.objects.all()
    serializer_class = DistrictDetailSerializer


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
def to_md5_hex(origin_str):
    """生成MD5摘要"""
    password = md5(origin_str.encode('utf-8')).hexdigest()
    return password


@api_view(['POST'])
def user_info(request):
    """完善个人信息（增加用户名和密码）"""
    user = request.session.get('user')
    # user = Users.objects.get(u_id=1)
    form = UserInfoForm(request.POST)
    if form.is_valid():
        user.u_nickname = form.cleaned_data['nickname']
        user.u_password = to_md5_hex(form.cleaned_data['password'])
        user.save()
        data = {'code': 200, 'message': '操作成功'}
        return JsonResponse(data=data)


@api_view(['POST'])
def order_finish_or_cancel(request):
    """完成订单或者取消订单"""
    order_number = request.data.get('order_number')
    status = request.data.get('order_status')
    order = Orders.objects.filter(order_number=order_number).first()
    if status == 0:
        order.order_status = 0
        order.save()
    else:
        order.order_status = 1
        order.save()
    data = {'code': 200, 'message': '操作成功'}
    return JsonResponse(data=data)
