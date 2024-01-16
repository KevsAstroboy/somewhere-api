from django.db import models
from .produit import Produit
from .commande import Commande


# Creation of commande produit model here.

class CommandeProduit(models.Model):
    # ----------------------------------------------------------------------
    # ENTITY DATA FIELDS
    # ----------------------------------------------------------------------

    prix_achat = models.FloatField(null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()

    # ----------------------------------------------------------------------
    # ENTITY LINKS ( RELATIONSHIP )
    # ----------------------------------------------------------------------

    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
