from django import forms
from .models import *

# 열람시간 폼
class OpenTimeForm(forms.ModelForm):
    class Meta:
        model = openTime
        fields = ['morning_time', 'night_time']
        widgets = {
            'morning_time': forms.TimeInput(attrs={'type': 'time'}),
            'night_time': forms.TimeInput(attrs={'type': 'time'}),
        }

# 메세지 폼
class MessageForm(forms.ModelForm):
    nickname = forms.CharField(label="닉네임", max_length=40)

    class Meta:
        model = Message
        fields = ['morning_mes', 'night_mes', 'nickname', 'group']
        labels = {
            'morning_mes': '아침메세지',
            'night_mes': '밤메세지',
            'group': '그룹',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user is not None:
            user_profile = Profile.objects.get(user=user)
            user_groups = Group.objects.filter(memberships__profile=user_profile)
            self.fields['group'].queryset = user_groups
            # 9:21 수정
            self.fields['group'].widget = forms.Select(choices=[(None, '전체')] + [(group.id, group.name) for group in user_groups])