import json

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action

from ..dao.entity.profil import Profil
from ..dao.entity.user import User
from ..serializers.user_serializer import UserSerializerToSave, UserSerializerToUpdate, UserSerializerToGet
from ..utils.contract.response import Response
from ..utils.dto.user_dto import UserDto
from ..utils.status import Status
from ..utils.utils import Utils


class UserBusiness(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerToSave

    @csrf_exempt
    @action(detail=False, methods=['post'], url_name='create')
    def create(self, request, *args, **kwargs):
        print("--------------- Begin create user -----------------------")
        response = Response[UserDto]()
        json_data = request.body.decode('utf-8')
        request_data = json.loads(json_data)
        dtos = request_data.get('datas', [])
        items = []
        for dto_data in dtos:
            serializer = UserSerializerToSave(data=dto_data)
            if serializer.is_valid():
                dto = serializer.create_user_dto(serializer.validated_data)
                # Effectuez le traitement et la validation ici pour chaque objet DTO

                if Utils.is_blank(dto.nom) or Utils.is_blank(dto.prenom) or Utils.is_blank(dto.login) or Utils.is_blank(
                        dto.password) or Utils.is_blank(dto.contact):
                    response.has_error = True
                    response.status = Status(code=500, message="Veuillez bien renseigner les champs obligatoires")
                    return JsonResponse(response.dict(),
                                        status=500)

                if dto.profil_id:
                    existing_profil = Profil.objects.filter(id=dto.profil_id, is_deleted=False).first()
                    if existing_profil is None:
                        response.has_error = True
                        response.status = Status(code=500, message="Ce profil n'existe pas")
                        return JsonResponse(response.dict(),
                                            status=500)  # Utilisez JsonResponse pour retourner un objet JSON

                if dto.login:
                    existing_login = User.objects.filter(login=dto.login, is_deleted=False).first()
                    if existing_login:
                        response.has_error = True
                        response.status = Status(code=500, message="Ce login existe déjà")
                        return JsonResponse(response.dict(),
                                            status=500)

                if dto.contact:
                    existing_contact = User.objects.filter(contact=dto.contact, is_deleted=False).first()
                    if existing_contact:
                        response.has_error = True
                        response.status = Status(code=500, message="Ce contact existe déjà")
                        return JsonResponse(response.dict(),
                                            status=500)
                if dto.matricule:
                    existing_matricule = User.objects.filter(contact=dto.matricule, is_deleted=False).first()
                    if existing_matricule:
                        response.has_error = True
                        response.status = Status(code=500, message="Ce mmatricule existe déjà")
                        return JsonResponse(response.dict(),
                                            status=500)
                if dto.password:
                    dto.password = make_password(dto.password)

                profil = Profil.objects.filter(id=dto.profil_id,
                                               is_deleted=False).first() if dto.profil_id is not None else Profil.objects.get(
                    id=1)

                dto.created_at = str(timezone.now())
                dto.created_by = 1

                # Créez un objet User à partir du DTO
                user = User(
                    nom=dto.nom,
                    prenom=dto.prenom,
                    matricule=dto.matricule,
                    login=dto.login,
                    password=dto.password,
                    contact=dto.contact,
                    profil=profil,
                    created_at=dto.created_at,
                    created_by=dto.created_by
                )

                # Sauvegardez le User
                user.save()

                # Ajouter un ProfilDto à la liste en excluant les champs avec des valeurs None
                items.append(UserDto(
                    id=user.id,
                    nom=user.nom,
                    prenom=user.prenom,
                    matricule=user.matricule,
                    login=user.login,
                    contact=user.contact,
                    profil_id=profil.id,
                    profil_libelle=profil.libelle,
                    is_deleted=user.is_deleted,
                    created_by=user.created_by,
                    created_at=str(profil.created_at),
                ))
            else:
                response.has_error = True
                response.status = Status(code=400, message="Validation de la requête a échoué")
                return JsonResponse(response.dict(), status=400)

        if items:
            response.has_error = False
            response.items = items
            response.count = len(items)
            print("--------------- End create user -----------------------")
            return JsonResponse(response.dict(), status=200)  # Utilisez JsonResponse pour retourner un objet JSON

        response.has_error = True
        response.status = Status(code=500, message="Liste de datas vide")
        return JsonResponse(response.dict(), status=500)

    @csrf_exempt
    @action(detail=False, methods=['put'], url_name='update')
    def update(self, request, *args, **kwargs):
        print("--------------- Begin update user -----------------------")
        response = Response[UserDto]()
        json_data = request.body.decode('utf-8')
        request_data = json.loads(json_data)
        dtos = request_data.get('datas', [])
        items = []
        for dto_data in dtos:
            serializer = UserSerializerToUpdate(data=dto_data)
            if serializer.is_valid():
                dto = serializer.create_user_dto(serializer.validated_data)
                if dto.id is None:
                    response.has_error = True
                    response.status = Status(code=500, message="Champ id obligatoire")
                    return JsonResponse(response.dict(),
                                        status=500)

                existing_user = User.objects.filter(id=dto.id).first()
                if existing_user is None:
                    response.has_error = True
                    response.status = Status(code=500, message="Cet utilisateur n'existe pas id -> " + str(dto.id))
                    return JsonResponse(response.dict(),
                                        status=500)

                if dto.profil_id:
                    existing_profil = Profil.objects.filter(id=dto.profil_id, is_deleted=False).first()
                    if existing_profil is None:
                        response.has_error = True
                        response.status = Status(code=500, message="Ce profil n'existe pas")
                        return JsonResponse(response.dict(),
                                            status=500)  # Utilisez JsonResponse pour retourner un objet JSON

                if dto.login:
                    existing_login = User.objects.filter(login=dto.login, is_deleted=False).first()
                    if existing_login:
                        response.has_error = True
                        response.status = Status(code=500, message="Ce login existe déjà")
                        return JsonResponse(response.dict(),
                                            status=500)

                if dto.matricule:
                    existing_matricule = User.objects.filter(login=dto.matricule, is_deleted=False).first()
                    if existing_matricule:
                        response.has_error = True
                        response.status = Status(code=500, message="Ce matricule existe déjà")
                        return JsonResponse(response.dict(),
                                            status=500)

                if dto.contact:
                    existing_contact = User.objects.filter(login=dto.contact, is_deleted=False).first()
                    if existing_contact:
                        response.has_error = True
                        response.status = Status(code=500, message="Ce contact existe déjà")
                        return JsonResponse(response.dict(),
                                            status=500)

                dto.updated_at = str(timezone.now())
                dto.updated_by = 1
                dto.deleted_by = None

                existing_user.updated_by = dto.updated_by
                existing_user.updated_at = dto.updated_at
                existing_user.deleted_by = dto.deleted_by
                existing_user.is_deleted = dto.is_deleted if dto.is_deleted is not None else False
                existing_user.is_locked = dto.is_locked if dto.is_locked is not None else False
                existing_user.nom = dto.nom if dto.nom is not None else existing_user.nom
                existing_user.prenom = dto.prenom if dto.prenom is not None else existing_user.prenom
                existing_user.matricule = dto.matricule if dto.matricule is not None else existing_user.matricule
                existing_user.login = dto.login if dto.login is not None else existing_user.login
                existing_user.contact = dto.contact if dto.contact is not None else existing_user.contact
                existing_user.profil = Profil.objects.filter(id=dto.profil_id,
                                                             is_deleted=False).first() if dto.profil_id is not None else existing_user.profil

                # Sauvegardez le user
                existing_user.save()

                # Ajouter un UserDto à la liste en excluant les champs avec des valeurs None
                items.append(UserDto(
                    id=existing_user.id,
                    nom=existing_user.nom,
                    prenom=existing_user.prenom,
                    matricule=existing_user.matricule,
                    login=existing_user.login,
                    contact=existing_user.contact,
                    profil_id=existing_user.profil.id,
                    profil_libelle=existing_user.profil.libelle,
                    is_deleted=existing_user.is_deleted,
                    created_by=existing_user.created_by,
                    created_at=str(existing_user.created_at),
                    updated_at=str(existing_user.updated_at),
                    updated_by=existing_user.updated_by,
                ))
            else:
                response.has_error = True
                response.status = Status(code=400, message="Validation de la requête a échoué")
                return JsonResponse(response.dict(), status=400)

        if items:
            response.has_error = False
            response.items = items
            response.count = len(items)
            print("--------------- End update user -----------------------")
            return JsonResponse(response.dict(), status=200)  # Utilisez JsonResponse pour retourner un objet JSON

        response.has_error = True
        response.status = Status(code=500, message="Liste de datas vide")
        return JsonResponse(response.dict(), status=500)

    @csrf_exempt
    @action(detail=False, methods=['delete'], url_name='delete')
    def delete(self, request, *args, **kwargs):
        print("--------------- Begin delete user -----------------------")
        response = Response[UserDto]()
        json_data = request.body.decode('utf-8')
        request_data = json.loads(json_data)
        dtos = request_data.get('datas', [])
        items = []
        for dto_data in dtos:
            serializer = UserSerializerToUpdate(data=dto_data)
            if serializer.is_valid():
                dto = serializer.create_user_dto(serializer.validated_data)
                if dto.id is None:
                    response.has_error = True
                    response.status = Status(code=500, message="Champ id obligatoire")
                    return JsonResponse(response.dict(),
                                        status=500)

                existing_user = User.objects.filter(id=dto.id).first()
                if existing_user is None:
                    response.has_error = True
                    response.status = Status(code=500, message="Cet utilisateur n'existe pas id -> " + str(dto.id))
                    return JsonResponse(response.dict(),
                                        status=500)

                dto.updated_at = str(timezone.now())
                dto.updated_by = 1

                existing_user.updated_by = dto.updated_by
                existing_user.updated_at = dto.updated_at
                existing_user.is_deleted = True

                # Sauvegardez le profil
                existing_user.save()

                # Ajouter un ProfilDto à la liste en excluant les champs avec des valeurs None
                items.append(UserDto(
                    id=existing_user.id,
                    nom=existing_user.nom,
                    prenom=existing_user.prenom,
                    matricule=existing_user.matricule,
                    login=existing_user.login,
                    contact=existing_user.contact,
                    profil_id=existing_user.profil.id,
                    profil_libelle=existing_user.profil.libelle,
                    is_deleted=existing_user.is_deleted,
                    created_by=existing_user.created_by,
                    created_at=str(existing_user.created_at),
                    updated_at=str(existing_user.updated_at),
                    updated_by=existing_user.updated_by,
                ))
            else:
                response.has_error = True
                response.status = Status(code=400, message="Validation de la requête a échoué")
                return JsonResponse(response.dict(), status=400)

        if items:
            response.has_error = False
            response.items = items
            response.count = len(items)
            print("--------------- End delete user -----------------------")
            return JsonResponse(response.dict(), status=200)  # Utilisez JsonResponse pour retourner un objet JSON

        response.has_error = True
        response.status = Status(code=500, message="Liste de datas vide")
        return JsonResponse(response.dict(), status=500)

    @csrf_exempt
    @action(detail=False, methods=['get'], url_name='get_by_criteria')
    def get_by_criteria(self, request, *args, **kwargs):
        print("--------------- Begin get_by_criteria user -----------------------")
        response = Response[UserDto]()
        json_data = request.body.decode('utf-8')
        request_data = json.loads(json_data)
        dtos = request_data.get('datas', [])
        items = []
        query = Q()
        for dto_data in dtos:

            serializer = UserSerializerToGet(data=dto_data)
            if serializer.is_valid():
                dto = serializer.create_user_dto(serializer.validated_data)

                if dto.nom:
                    query &= Q(nom=dto.nom)
                if dto.prenom:
                    query &= Q(prenom=dto.prenom)
                if dto.id:
                    query &= Q(id=dto.id)
                if dto.matricule:
                    query &= Q(matricule=dto.matricule)
                if dto.login:
                    query &= Q(login=dto.login)
                if dto.contact:
                    query &= Q(contact=dto.contact)
                if dto.profil_id:
                    query &= Q(profil__id=dto.profil_id)
                if dto.profil_libelle:
                    query &= Q(profil__libelle=dto.profil_libelle)
                if dto.is_deleted is not None:
                    query &= Q(is_deleted=dto.is_deleted)
                if dto.is_locked is not None:
                    query &= Q(is_locked=dto.is_locked)

                if dto.created_at:
                    try:
                        created_at_date = datetime.strptime(dto.created_at, "%d/%m/%Y %H:%M:%S")
                        query &= Q(created_at=created_at_date)
                    except ValueError:
                        pass
                # Convertir la date au format "dd/mm/YYYY" en objet datetime
                if dto.updated_at:
                    try:
                        updated_at_date = datetime.strptime(dto.updated_at, "%d/%m/%Y %H:%M:%S")
                        query &= Q(updated_at=updated_at_date)
                    except ValueError:
                        pass

                if dto.updated_by:
                    query &= Q(updated_by=dto.updated_by)
                if dto.deleted_by:
                    query &= Q(deleted_by=dto.deleted_by)
                if dto.created_by:
                    query &= Q(deleted_by=dto.created_by)

                users = User.objects.filter(query)


                for user in users:
                    # Ajouter un ProfilDto à la liste en excluant les champs avec des valeurs None
                    items.append(UserDto(
                        id=user.id,
                        nom=user.nom,
                        prenom=user.prenom,
                        matricule=user.matricule,
                        login=user.login,
                        contact=user.contact,
                        profil_id=user.profil.id,
                        profil_libelle=user.profil.libelle,
                        is_deleted=user.is_deleted,
                        created_by=user.created_by,
                        created_at=str(user.created_at),
                        updated_at=str(user.updated_at),
                        updated_by=user.updated_by,
                    ))
            else:
                response.has_error = True
                response.status = Status(code=400, message="Validation de la requête a échoué")
                return JsonResponse(response.dict(), status=400)

        if items:
            response.has_error = False
            response.items = items
            response.count = len(items)
            print("--------------- End get_by_criteria user -----------------------")
            return JsonResponse(response.dict(), status=200)  # Utilisez JsonResponse pour retourner un objet JSON

        response.has_error = True
        response.status = Status(code=500, message="Liste de datas vide")
        return JsonResponse(response.dict(), status=500)
