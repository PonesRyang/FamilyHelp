import uuid

from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.models import Users, District, Orders
from api.serializers import DistrictSerializer





class DistrictViewSet(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


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




