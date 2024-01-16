from django.db import models

from .produit import Produit


# Creation of produit photo model here.

class ProduitPhoto(models.Model):
    # ----------------------------------------------------------------------
    # ENTITY DATA FIELDS
    # ----------------------------------------------------------------------

    photo = models.FileField(upload_to='product_pics')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    deleted_by = models.IntegerField()

    # ----------------------------------------------------------------------
    # ENTITY LINKS ( RELATIONSHIP )
    # ----------------------------------------------------------------------

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
