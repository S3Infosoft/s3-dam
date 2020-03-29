from . import resources
from enquiry import models
from users.models import GlobalInfo

from django.core.cache import cache
from django.template.loader import get_template

from datetime import datetime
from io import BytesIO

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dic: dict):
    template = get_template(template_src)

    global_obj = GlobalInfo.objects.first()

    context_dic["logo"] = global_obj.logo
    context_dic["address"] = global_obj.address

    html = template.render(context_dic)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result


def generate_csv(start_date: datetime.date,
                 end_date: datetime.date,
                 model: str):

    # keys to get data from cache
    key = f"{model}-{start_date}-{end_date}"

    q = cache.get(key)

    if not q:
        # pr is the import-export object for respective model
        if model == "OTA":
            pr = resources.OTAResource()
            q = models.OTA.objects.filter(registration__date__gte=start_date,
                                          registration__date__lte=end_date)
        elif model == "PARTNER":
            pr = resources.PartnerResource()
            q = models.Partner.objects.filter(created__date__gte=start_date,
                                              created__date__lte=end_date)
        else:
            pr = resources.ReviewResource()
            q = models.Review.objects.filter(created__date__gte=start_date,
                                             created__date__lte=end_date)
        cache.set(key, q)
    else:
        if model == "OTA":
            pr = resources.OTAResource()
        elif model == "PARTNER":
            pr = resources.PartnerResource()
        else:
            pr = resources.ReviewResource()

    csv = pr.export(q)
    return csv


def generate_pdf(start_date: datetime.date,
                 end_date: datetime.date,
                 model: str):
    key = f"{model}-{start_date}-{end_date}"

    q = cache.get(key)

    if not q:
        if model == "OTA":
            q = models.OTA.objects.filter(registration__date__gte=start_date,
                                          registration__date__lte=end_date)
            template = "activities/ota_pdf.html"
        elif model == "PARTNER":
            q = models.Partner.objects.filter(created__date__gte=start_date,
                                              created__date__lte=end_date)
            template = "activities/partner_pdf.html"
        else:
            q = models.Review.objects.filter(created__date__gte=start_date,
                                             created__date__lte=end_date)
            template = "activities/review_pdf.html"

        cache.set(key, q)
    else:
        if model == "OTA":
            template = "activities/ota_pdf.html"
        elif model == "PARTNER":
            template = "activities/partner_pdf.html"
        else:
            template = "activities/review_pdf.html"

    pdf = render_to_pdf(template, {"objects": q,
                                   "title": model,
                                   "start_date": start_date,
                                   "end_date": end_date})
    return pdf
