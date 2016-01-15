from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from report.forms import ReportForm, Item1Form, Item2Form, Item3Form, UserCreationForm
from report.models import Report
from items.models import Items
from django.template import RequestContext
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

@login_required(login_url="/users/login/")
def report_list(request):
    reports = Report.objects.filter(user_id=request.user)
    return render(request, 'report_list.html', {'reports': reports})

def detail_report(request, pk):
    detail = get_object_or_404(Report, pk=pk)
    stage1_obj = Items.objects.filter(stage=1,report_id=pk)
    stage2_obj = Items.objects.filter(stage=2,report_id=pk)
    stage3_obj = Items.objects.filter(stage=3,report_id=pk)
    return render(request, 'report_detail.html', {'detail': detail,'stage1_obj':stage1_obj,'stage2_obj':stage2_obj,'stage3_obj':stage3_obj})

def create_report(request):
    if request.method == 'POST':

        form = ReportForm(request.POST)
        print "hello"
        if form.is_valid(): #check rules in forms.py
            report_name = request.POST.get('report_name') #from html
            report_obj = Report(name=report_name) #get data into Report Model
            report_obj.user_id = request.user #from user that login
            report_obj.save() #save data intp database


            item_stage1_name = request.POST.getlist('stage1')
            for item in item_stage1_name:
                if item != '':
                    item_obj = Items(name=item, stage=1, report_id=report_obj)
                    item_obj.save()

            item_stage2_name = request.POST.getlist('stage2')
            for item in item_stage2_name:
                if item != '':
                    item_obj = Items(name=item, stage=2, report_id=report_obj)
                    item_obj.save()

            item_stage3_name = request.POST.getlist('stage3')
            for item in item_stage3_name:
                if item != '':
                    item_obj = Items(name=item, stage=3, report_id=report_obj)
                    item_obj.save()

            if request.POST.get("check_default",False):
                Items.objects.bulk_create([
                    Items(name="Do I know what topic I would like to write?", stage=1, report_id=report_obj),
                    Items(name="Do I have enough information to write?", stage=1, report_id=report_obj),
                    Items(name="Does the report have the title?", stage=2, report_id=report_obj),
                    Items(name="Does the report have the table of content?", stage=2, report_id=report_obj),
                    Items(name="Does the report have the content?", stage=2, report_id=report_obj),
                    Items(name="Does the report have the references?", stage=2, report_id=report_obj),
                    Items(name="Do I send an email to my lecturer that I complete the report?",stage=3, report_id=report_obj),
                    Items(name="Do I post it on my Facebook?", stage=3, report_id=report_obj),
                ])

            return HttpResponseRedirect(reverse('report.views.create_report')) #redirect after POST
    else:
        form = ReportForm()
    return render(request, 'create_report.html', {})

def page_stage1(request, pk):
    if request.method == "POST":
        items_pk = request.POST.getlist('check')
        for item_pk in items_pk:
            item_obj = get_object_or_404(Items, pk=item_pk)
            item_obj.status = True
            item_obj.save()
        items_obj = Items.objects.filter(stage=1,report_id=pk)
        if all(item.status == 1 for item in items_obj ) == True:
            return HttpResponseRedirect(reverse("report.views.page_stage2", args=(),
    kwargs={'pk': pk }))

    report_obj = get_object_or_404(Report, pk=pk)
    stage1 = Items.objects.filter(stage=1,report_id=report_obj)
    return render(request, 'stage1.html', {'stage1': stage1, 'report_obj': report_obj},)

def page_stage2(request, pk):
    if request.method == "POST":
        items_pk = request.POST.getlist('check')
        for item_pk in items_pk:
            item_obj = get_object_or_404(Items, pk=item_pk)
            item_obj.status = True
            item_obj.save()
        items_obj = Items.objects.filter(stage=2,report_id=pk)
        if all(item.status == 1 for item in items_obj ) == True:
            return HttpResponseRedirect(reverse("report.views.page_stage3", args=(),
    kwargs={'pk': pk }))

    report_obj = get_object_or_404(Report, pk=pk)
    stage2 = Items.objects.filter(stage=2,report_id=report_obj)
    return render(request, 'stage2.html', {'stage2': stage2, 'report_obj': report_obj},)

def page_stage3(request, pk):
    if request.method == "POST":
        items_pk = request.POST.getlist('check')
        for item_pk in items_pk:
            item_obj = get_object_or_404(Items, pk=item_pk)
            item_obj.status = True
            item_obj.save()
        items_obj = Items.objects.filter(stage=3,report_id=pk)
        if all(item.status == 1 for item in items_obj ) == True:
            return HttpResponseRedirect(reverse("report.views.report_list"))

    report_obj = get_object_or_404(Report, pk=pk)
    stage3 = Items.objects.filter(stage=3,report_id=report_obj)
    return render(request, 'stage3.html', {'stage3': stage3, 'report_obj': report_obj},)


def edit_report(request,pk):
    report_obj = get_object_or_404(Report, pk=pk)
    stage1_obj = Items.objects.filter(stage=1,report_id=pk)
    stage2_obj = Items.objects.filter(stage=2,report_id=pk)
    stage3_obj = Items.objects.filter(stage=3,report_id=pk)
    return render(request, 'edit_report.html', {'report_obj':report_obj,'stage1_obj':stage1_obj,'stage2_obj':stage2_obj,'stage3_obj':stage3_obj})

def delete_item(request,report_id, item_id):
    item = Items.objects.get(pk=item_id).delete()
    return HttpResponseRedirect(reverse("report.views.edit_report", args=(),
kwargs={'pk': report_id }))

def add_item(request,report_id):
    if request.method == 'POST':
        form_1 = Item1Form(request.POST)
        form_2 = Item2Form(request.POST)
        form_3 = Item3Form(request.POST)

        if form_1.is_valid():
            item_stage1 = request.POST.getlist('item_stage1_name')
            for item in item_stage1:
                if item != '':
                    report_obj = Report(pk=report_id)
                    item_obj = Items(name=item, stage=1, report_id=report_obj)
                    item_obj.save()

        elif form_2.is_valid():
            item_stage2 = request.POST.getlist('item_stage2_name')
            for item in item_stage2:
                if item != '':
                    report_obj = Report(pk=report_id)
                    item_obj = Items(name=item, stage=2, report_id=report_obj)
                    item_obj.save()

        elif form_3.is_valid():
            item_stage3 = request.POST.getlist('item_stage3_name')
            for item in item_stage3:
                if item != '':
                    report_obj = Report(pk=report_id)
                    item_obj = Items(name=item, stage=3, report_id=report_obj)
                    item_obj.save()


        return HttpResponseRedirect(reverse("report.views.edit_report", args=(), kwargs={'pk': report_id }))
