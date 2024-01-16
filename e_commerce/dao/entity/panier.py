from django.db import models
from .user import User
from .produit import Produit


# Creation of panier model here.

class Panier(models.Model):
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

    # ----------------------------------------------------------------------
    # ENTITY LINKS ( RELATIONSHIP )
    # ----------------------------------------------------------------------

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    produits = models.ManyToManyField(Produit)
