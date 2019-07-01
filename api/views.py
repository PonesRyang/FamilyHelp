from hashlib import md5

from django.http import JsonResponse

# Create your views here.
from rest_framework.decorators import api_view

from api.forms import UserInfoForm
from api.models import Orders, Users


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

