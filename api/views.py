from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from api.filters import OrderFilterSet
from api.models import Orders, Users, Comment, Complain, OrderComplain
from api.serializers import OrderDetailSerializer


class OrderViewsSet(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderDetailSerializer
    filter_backends = (OrderingFilter, )
    ordering = ('-order_createtime', )

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







