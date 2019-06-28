from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view

from api.models import Users


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

