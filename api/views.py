from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from api.filters import OrderFilterSet
from api.models import Orders, Users, Comment
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
        user1 = request.data.get('user', '')
        order = request.data.get('order_id', '')
        user =






