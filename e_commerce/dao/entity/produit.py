from django.db import models
from .categorie import Categorie
from .discount import Discount


# Creation of produit model here.

class Produit(models.Model):

    # ----------------------------------------------------------------------
    # ENTITY DATA FIELDS
    # ----------------------------------------------------------------------
    nom = models.CharField(max_length=225, null=True)
    description = models.CharField(max_length=225, null=True)
    prix_ht = models.FloatField(null=True)
    prix_ttc = models.FloatField(null=False)
    poids = models.FloatField(null=True)
    stock = models.IntegerField(null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()

    # ----------------------------------------------------------------------
    # ENTITY LINKS ( RELATIONSHIP )
    # ----------------------------------------------------------------------

    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=False)
    discount = models.OneToOneField(Discount, on_delete=models.SET_NULL, null=True)
