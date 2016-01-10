from django import forms

class ReportForm(forms.Form):
    report_name = forms.CharField()
    check_default = forms.BooleanField()
class Item1Form(forms.Form):
    item_stage1_name = forms.CharField()

class Item2Form(forms.Form):
    item_stage2_name = forms.CharField()

class Item3Form(forms.Form):
    item_stage3_name = forms.CharField(required=True)
