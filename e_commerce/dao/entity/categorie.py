from django.db import models


# Creation of categorie model here.

class Categorie(models.Model):

    # ----------------------------------------------------------------------
    # ENTITY DATA FIELDS
    # ----------------------------------------------------------------------

    code = models.CharField(max_length=225, null=True)
    libelle = models.CharField(max_length=225, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    deleted_by = models.IntegerField()
