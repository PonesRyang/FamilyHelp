import re

from django import forms
from django.core.exceptions import ValidationError

from api.models import Users


class UserInfoForm(forms.Form):
    nickname = forms.CharField(min_length=5, max_length=10)
    password = forms.CharField(min_length=5)

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        patten = re.compile(r'\w{5,10}')
        if not patten.fullmatch(nickname):
            raise ValidationError('用户名由5到10的数字、下划线或者字母组成')
        user = Users.objects.filter(u_nickname=nickname).first()
        if user:
            raise ValidationError('用户名已存在')
        return nickname

    def clean_password(self):
        password = self.cleaned_data['password']
        lenght = len(password)
        if lenght > 5:
            return password
        raise ValidationError('密码长度不能小于5')