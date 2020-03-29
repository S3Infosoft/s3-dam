from . import utils
from schedules.models import Schedule

from django.core.mail import EmailMessage

from background_task import background

from datetime import datetime
import json

import requests


@background(schedule=1)
def get_ota_data(obj_id, search_text, check_in_date, check_out_date, ota_name):
    search_text = search_text
    ota = ota_name
    check_in_date = check_in_date
    check_out_date = check_out_date

    data = f'{{"search_text":"{search_text}", "checkin_date": ' \
        f'"{check_in_date}", "checkout_date": "{check_out_date}" }}'
    headers = {'Content-Type': 'application/json'}
    url = "http://mvr-fe_mvrautomation_1:5000/automation/v1/{}".format(
        ota.lower()
    )
    res = requests.post(url, headers=headers, data=data)
    schedule = Schedule.objects.get(id=obj_id)

    if res.status_code == 200:
        res_data = json.loads(res.content.decode("utf-8"))
        price = {"Std_CP": res_data["Std_CP"],
                 "Std_EP": res_data["Std_EP"],
                 "Sup_CP": res_data["Sup_CP"],
                 "Sup_EP": res_data["Sup_EP"]}
        schedule.status = "FINISHED"
        schedule.listing_position_number = res_data["listed_position"]
        schedule.room_category_and_rates = price
    else:
        schedule.status = "FAILED"

    schedule.save()


@background(schedule=1)
def email_report(subject, message, sender, recipient,
                 s_day, s_month, s_year, e_day, e_month, e_year, model):

    start_date = datetime(year=s_year, month=s_month, day=s_day).date()
    end_date = datetime(year=e_year, month=e_month, day=e_day).date()

    email = EmailMessage(
        subject,
        message,
        sender,
        [recipient])

    csv = utils.generate_csv(start_date, end_date, model)
    pdf = utils.generate_pdf(start_date, end_date, model)

    name = f"{model}-{start_date} {end_date}"

    email.attach(f"{name}.csv",
                 csv.csv,
                 "text/csv")
    email.attach(f"{name}.pdf",
                 pdf.getvalue(),
                 "text/pdf")
    email.send()
