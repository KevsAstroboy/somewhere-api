from django.db import models


# Creation of brand model here.

class Brand(models.Model):
    # ----------------------------------------------------------------------
    # ENTITY DATA FIELDS
    # ----------------------------------------------------------------------

    nom = models.CharField(max_length=225, null=True)
    logo = models.FileField(upload_to='brand')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    deleted_by = models.IntegerField()
