from django.db import models
from .user import User
from .produit import Produit
from django.utils.translation import gettext_lazy as _


# Creation of commande model here.

class Commande(models.Model):
    STATUS_CHOICES = (
        ('canceled', _('Annulé')),
        ('in_progress', _('En cours')),
        ('paid', _('payé')),
    )
    # ----------------------------------------------------------------------
    # ENTITY DATA FIELDS
    # ----------------------------------------------------------------------
    code = models.CharField(max_length=225, null=True)
    libelle = models.CharField(max_length=225, null=True)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES)
    is_deleted = models.BooleanField(default=False)
    lieu_livraison = models.CharField(max_length=225, null=True)
    contact_livraison = models.CharField(max_length=225, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()

    # ----------------------------------------------------------------------
    # ENTITY LINKS ( RELATIONSHIP )
    # ----------------------------------------------------------------------

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    produits = models.ManyToManyField(Produit, through='CommandeProduit')
