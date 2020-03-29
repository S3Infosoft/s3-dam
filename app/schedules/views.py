from . import forms
from activities.tasks import get_ota_data
from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required
def schedule(request):
    if request.method == "POST":
        form = forms.ScheduleHandlingForm(request.POST)
        if form.is_valid():
            form.instance.creator = request.user
            sc = form.save()

            cd = form.cleaned_data
            search_text = request.POST.get("search_text")
            check_in_date = cd["check_in_date"].date().strftime("%d/%m/%Y")
            check_out_date = cd["check_out_date"].date().strftime("%d/%m/%Y")
            ota_name = cd["ota_name"].name

            get_ota_data(sc.id, search_text,
                         check_in_date, check_out_date, ota_name)
            messages.add_message(request, messages.SUCCESS,
                                 "Your schedule ID is {}".format(sc.id))
            return HttpResponseRedirect(request.path)

    else:
        form = forms.ScheduleHandlingForm()
    return render(request,
                  "schedules/schedule_handling.html",
                  {"form": form})


@login_required
def display_schedule(request):
    return render(request, "schedules/scheduled.html")
