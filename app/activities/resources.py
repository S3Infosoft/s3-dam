from enquiry import models
from import_export import resources


class OTAResource(resources.ModelResource):
    class Meta:
        model = models.OTA
        exclude = "id", "update"


class PartnerResource(resources.ModelResource):
    class Meta:
        model = models.Partner
        exclude = "id", "update"

    def __init__(self):
        super(PartnerResource, self).__init__()
        self.fields["partner_type"].attribute = "get_partner_type_display"


class ReviewResource(resources.ModelResource):
    class Meta:
        model = models.Review
        exclude = "id", "update"

    def __init__(self):
        super(ReviewResource, self).__init__()
        self.fields["rating"].attribute = "get_rating_display"
