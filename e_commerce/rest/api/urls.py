from django.urls import path
from ...business.profil_business import ProfilBusiness
from ...business.user_business import UserBusiness

profil_business = ProfilBusiness.as_view({
    'post': 'create',
    'put': 'update',
    'delete': 'delete',
    'get': 'get_by_criteria',
})

user_business = UserBusiness.as_view({
    'post': 'create',
    'put': 'update',
    'delete': 'delete',
    'get': 'get_by_criteria',
})

urlpatterns = [
    # Profil endpoint

    path('profil/create/', profil_business, name='create_profil'),
    path('profil/update/', profil_business, name='update_profil'),
    path('profil/delete/', profil_business, name='delete_profil'),
    path('profil/get_by_criteria/', profil_business, name='get_profil'),

    # User endpoint

    path('user/create/', user_business, name='create_user'),
    path('user/update/', user_business, name='update_user'),
    path('user/delete/', user_business, name='delete_user'),
    path('user/get_by_criteria/', user_business, name='get_user'),
]
