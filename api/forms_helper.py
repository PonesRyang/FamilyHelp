import re

from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    tel = forms.CharField(min_length=11, max_length=11)
    captcha = forms.CharField(min_length=4, max_length=4)
    # phoneCode = forms.CharField(min_length=6, max_length=6)

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        pattern = re.compile(r'\d{11}')
        if not pattern.fullmatch(tel):
            raise ValidationError('请输入有效手机号')
        return tel
