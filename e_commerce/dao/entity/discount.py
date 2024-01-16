from django.db import models


# Creation of categorie model here.

class Discount(models.Model):

    # ----------------------------------------------------------------------
    # ENTITY DATA FIELDS
    # ----------------------------------------------------------------------

    name = models.CharField(max_length=225, null=True)
    description = models.CharField(max_length=225, null=True)
    coupon_code = models.CharField(max_length=225, null=True)
    percent = models.FloatField(null=False)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    valid_until = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    deleted_by = models.IntegerField()
