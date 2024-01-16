from django.contrib import admin

from .dao.entity.brand import Brand
from .dao.entity.profil import Profil
from .dao.entity.commande import Commande
from .dao.entity.panier import Panier
from .dao.entity.produit import Produit
from .dao.entity.commande_produit import CommandeProduit
from .dao.entity.user import User
from .dao.entity.categorie import Categorie
from .dao.entity.discount import Discount
from .dao.entity.photo_produit import ProduitPhoto


# Register your models here.

admin.register(Brand)
admin.register(Profil)
admin.register(Commande)
admin.register(Panier)
admin.register(Produit)
admin.register(CommandeProduit)
admin.register(User)
admin.register(Categorie)
admin.register(Discount)
admin.register(ProduitPhoto)
