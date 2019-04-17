from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', ]
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'introduction', ]
        
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):   # Meta class도 상속받을 수 있다
        model = get_user_model()
        fields = UserCreationForm.Meta.fields    # 상속받는 것 가져와야 함