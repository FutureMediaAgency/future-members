from django import forms
from .models import Member


class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = "__all__"
