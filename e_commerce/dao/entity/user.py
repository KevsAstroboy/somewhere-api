from django.db import models
from .profil import Profil


# Creation of user model here.

class User(models.Model):
    # ----------------------------------------------------------------------
    # ENTITY DATA FIELDS
    # ----------------------------------------------------------------------

    nom = models.CharField(max_length=225, null=True)
    prenom = models.CharField(max_length=225, null=True)
    matricule = models.CharField(max_length=225, null=True)
    login = models.CharField(max_length=225, null=True)
    password = models.CharField(max_length=225, null=True)
    contact = models.CharField(max_length=225, null=True)
    is_deleted = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)

    # ----------------------------------------------------------------------
    # ENTITY LINKS ( RELATIONSHIP )
    # ----------------------------------------------------------------------

    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, null=False)
