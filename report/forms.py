from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ReportForm(forms.Form):
    report_name = forms.CharField()
    check_default = forms.BooleanField()
class Item1Form(forms.Form):
    item_stage1_name = forms.CharField()

class Item2Form(forms.Form):
    item_stage2_name = forms.CharField()

class Item3Form(forms.Form):
    item_stage3_name = forms.CharField(required=True)

class UserCreateForm(UserCreationForm):
    email = forms.CharField(required=True)

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
