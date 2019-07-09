import datetime
import uuid
from time import timezone

from captcha import Captcha
from utils import random_captcha_text, random_mobile_code, send_code_by_sms
from django.core.cache import caches
from api.forms_helper import LoginForm
from rest_framework.response import Response
from django.shortcuts import render, redirect
from hashlib import md5
from django.db.transaction import atomic
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view

from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.models import Users, Article, Comment, Complain, OrderComplain, Orders, Roles, OrderType, District, \
    StarArticle, Wallet, UserOrderList, Userrole
from api.serializers import ArticleSerializer, OrderDetailSerializer, StarStaffSerializer, OrdersTypeSerializer, \
    DistrictSimpleSerializer, \
    DistrictDetailSerializer, WalletSerializer

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from api.filters import OrderFilterSet, StarStaffFilterSet
from api.forms import UserInfoForm


def get_captcha(request):
    """ 验证码 """
    captcha_text = random_captcha_text()
    request.session['captcha'] = '1234'
    image_data = Captcha.instance().generate(captcha_text)
    return HttpResponse(image_data, content_type='image/png')


def send_mobile_code(request, tel):
    """发送短信验证码"""
    # code = random_mobile_code()
    # if tel in caches['mobile']:
    #     data = {'code': 403, 'message': '请不要在120秒内重复发送'}
    # else:
    #     result = send_code_by_sms(tel, code)
    #     if result['error'] == 0:
    #         # 将手机验证码保存到缓存中
    #         caches['mobile'].set(tel, code, timeout=120)
    #         data = {'code': 200, 'message': '短信验证码已发送'}
    #     else:
    #         data = {'code': 404, 'message': '短信验证码服务暂时无法使用'}
    try:
        code = '123456'
        request.session['tel'] = code
        data = {'code': 200, 'message': '短信验证码已发送成功'}
    except:
        data = {'code': 201, 'message': '短信验证码未发送成功'}
    return JsonResponse(data)


# @api_view(['GET','POST'])
# def register(request):
# 	if request.method=='GET':
# 		pass
# 	if request.method=='POST':
# 		pass


@api_view(['POST'])
def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        captcha_from_user = form.cleaned_data['captcha']
        captcha_from_sess = request.session.get('captcha', '')
        if captcha_from_sess.lower() != captcha_from_user.lower():
            data = {'code': 302, 'message': '验证码不匹配'}
        else:
            tel = form.cleaned_data['tel']
            user = Users.objects.filter(u_tel=tel).first()
            if user:
                code_from_session = request.session.get('tel')
                code_from_user = request.POST.get('phoneCode')
                if code_from_session == code_from_user:
                    request.session['user'] = user
                    data = {'code': 200, 'message': '校验成功'}
                else:
                    hint = '用户名或验证码错误'
                    data = {'code': 300, 'message': hint}
            else:
                with atomic():
                    user = Users()
                    user.u_tel = tel
                    user.u_nickname = '用户{}'.format(uuid.uuid4())
                    role = Roles.objects.filter(id=1).first()
                    user_role = Userrole()
                    user_role.role = role
                    user_role.user = user
                    user.save()
                    user_role.save()
                    wallet = Wallet()
                    wallet.money_int = 0
                    wallet.money_decimal = 0
                    wallet.save()
                    user.id = wallet
                    request.session['user'] = user
                    data = {'code': 201, 'message': '用户注册成功，成功登陆'}
    else:
        hint = '请输入有效的登录信息'
        data = {'code': 301, 'message': hint}
    return JsonResponse(data)


class DistrictViewSet(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSimpleSerializer


@api_view(['POST'])
def SubmitList(request):
    order_addr = request.data.get('order_addr')
    order_plantime = request.data.get('order_plantime')
    district = request.data.get('district')
    order_money = request.data.get('order_money')
    type_name = request.data.get('order_type')
    order_tips = request.data.get('order_tips')
    order_type = OrderType.objects.filter(order_type_name=type_name).first()
    district1 = District.objects.filter(name=district).first()
    user = request.session.get('user')
    if order_addr and order_plantime:
        order = Orders()
        order.order_money = order_money
        order.order_addr = order_addr
        order.order_plantime = order_plantime
        order.district = district1
        order.order_status = 2
        order.order_number = uuid.uuid4().hex
        order.order_type = order_type
        order.order_tips = order_tips
        order.save()
        user_order = UserOrderList()
        user_order.u = user
        user_order.order = order
        user_order.save()
        data = {
            'code': 200, 'message': '订单已生成'
        }
    else:
        data = {
            'code': 300, 'message': '订单地址不能为空'
        }
    return Response(data)


class StarStaffView(ListAPIView):
    """查看星级家政人员"""
    queryset = Users.objects.all()
    serializer_class = StarStaffSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = StarStaffFilterSet

    def get_queryset(self):
        role = Roles.objects.filter(r_code=1).first()
        queryset = Users.objects.filter(role=role).all()
        return queryset


class OrdersTypeViewSet(ModelViewSet):
    queryset = OrderType.objects.all()
    serializer_class = OrdersTypeSerializer
    pagination_class = None


# 获取所有省级行政单位 - GET /api/districts/
class ProvinceView(ListAPIView):
    """查看各省的id和名称"""
    # only defer 优化SQL查询
    queryset = District.objects.filter(parent__isnull=True).only('distid', )
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
        # u_id = self.request.session['user'].u_id
        self.queryset = Orders.objects.filter(users=self.request.session.get('user')).all()
        return self.queryset


@api_view(['POST'])
def comments(request):
    try:
        user = request.session['user']
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
        user1 = request.session['user']
        order_number = request.data.get('order_number', None)
        complain_content = request.data.get('complain_content', None)
        order = Orders.objects.filter(order_number=order_number).first()
        users = order.users_set.all()
        user2 = ''
        for user in users:
            if user.u_id != user1.u_id:
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
    if user.u_nickname and user.u_password:
        return JsonResponse(data={'code': 300, 'mes': '信息已完善，若需修改信息请调用修改信息接口'})
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
    order_number = request.POST.get('order_number')
    status = request.POST.get('order_status')
    order = Orders.objects.filter(order_number=order_number).first()
    status = int(status)
    if status == 0:
        order.order_status = 0
        order.order_finishtime = datetime.datetime.now()
        order.save()
        data = {'code': 200, 'message': '取消成功'}
    else:
        order.order_status = 1
        order.save()
        order.order_finishtime = datetime.datetime.now()
        data = {'code': 200, 'message': '操作成功'}
    return JsonResponse(data=data)


@api_view(['POST'])
def add_star_article(request):
    # try:
    with atomic():
        new_star = StarArticle()
        new_star.article = Article.objects.filter(ar_id=request.data.get('article_id')).first()
        new_star.star = request.data.get('article_star')
        new_star.user = request.session['user']
        # new_star.user = Users.objects.filter(u_id=1).first()
        new_star.save()
        data = {'code': 200, 'mes': '评价成功'}
    # except:
    # 	data = {'code':400,'mes':'评价失败，请重试'}
    return JsonResponse(data)


class WalletAPIView(ListAPIView):
    serializer_class = WalletSerializer
    pagination_class = None

    def get_queryset(self):
        return Wallet.objects.filter(users=self.request.session['user'])
#
