from datetime import datetime

from rest_framework.decorators import action
from rest_framework import viewsets

from ..dao.entity.profil import Profil
from ..serializers.profil_serializer import ProfilDtoSerializerToUpdate, ProfilDtoSerializerToGet
from ..utils.contract.response import Response
from ..utils.dto.profil_dto import ProfilDto
from ..utils.status import Status
from ..utils.utils import Utils
from ..serializers.profil_serializer import ProfilDtoSerializerToSave
from django.http import JsonResponse
import random
import string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q


class ProfilBusiness(viewsets.ModelViewSet):
    queryset = Profil.objects.all()
    serializer_class = ProfilDtoSerializerToSave

    @csrf_exempt
    @action(detail=False, methods=['post'], url_name='create')
    def create(self, request, *args, **kwargs):
        print("--------------- Begin create profil -----------------------")
        response = Response[ProfilDto]()
        json_data = request.body.decode('utf-8')
        request_data = json.loads(json_data)
        dtos = request_data.get('datas', [])
        items = []
        for dto_data in dtos:
            serializer = ProfilDtoSerializerToSave(data=dto_data)
            if serializer.is_valid():
                dto = serializer.create_profil_dto(serializer.validated_data)
                # Effectuez le traitement et la validation ici pour chaque objet DTO

                if Utils.is_blank(dto.code):
                    # Générer un code alphanumérique aléatoire
                    generated_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))
                    dto.code = "S-" + generated_code

                existing_profil = Profil.objects.filter(code=dto.code).first()
                if existing_profil:
                    response.has_error = True
                    response.status = Status(code=500, message="Cette donnée existe déjà")
                    return JsonResponse(response.dict(),
                                        status=500)  # Utilisez JsonResponse pour retourner un objet JSON

                dto.created_at = str(timezone.now())
                dto.created_by = 1

                # Créez un objet Profil à partir du DTO
                profil = Profil(
                    code=dto.code,
                    libelle=dto.libelle,
                    is_deleted=dto.is_deleted,
                    created_at=dto.created_at,
                    created_by=dto.created_by
                )

                # Sauvegardez le profil
                profil.save()

                # Ajouter un ProfilDto à la liste en excluant les champs avec des valeurs None
                items.append(ProfilDto(
                    id=profil.id,
                    code=profil.code,
                    libelle=profil.libelle,
                    is_deleted=profil.is_deleted,
                    created_by=profil.created_by,
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
            print("--------------- End create profil -----------------------")
            return JsonResponse(response.dict(), status=200)  # Utilisez JsonResponse pour retourner un objet JSON

        response.has_error = True
        response.status = Status(code=500, message="Liste de datas vide")
        return JsonResponse(response.dict(), status=500)

    @csrf_exempt
    @action(detail=False, methods=['put'], url_name='update')
    def update(self, request, *args, **kwargs):
        print("--------------- Begin update profil -----------------------")
        response = Response[ProfilDto]()
        json_data = request.body.decode('utf-8')
        request_data = json.loads(json_data)
        dtos = request_data.get('datas', [])
        items = []
        for dto_data in dtos:
            serializer = ProfilDtoSerializerToUpdate(data=dto_data)
            if serializer.is_valid():
                dto = serializer.create_profil_dto(serializer.validated_data)
                if dto.id is None:
                    response.has_error = True
                    response.status = Status(code=500, message="Champ id obligatoire")
                    return JsonResponse(response.dict(),
                                        status=500)

                existing_profil = Profil.objects.filter(id=dto.id).first()
                if existing_profil is None:
                    response.has_error = True
                    response.status = Status(code=500, message="Ce profil n'existe pas id -> " + str(dto.id))
                    return JsonResponse(response.dict(),
                                        status=500)

                if dto.code:
                    existing_profil = Profil.objects.filter(code=dto.code).first()
                    if existing_profil:
                        response.has_error = True
                        response.status = Status(code=500, message="Ce code profil existe déjà")
                        return JsonResponse(response.dict(),
                                            status=500)

                dto.updated_at = str(timezone.now())
                dto.updated_by = 1

                profil = Profil.objects.get(id=dto.id)
                if profil is None:
                    response.has_error = True
                    response.status = Status(code=500, message="Ce profil n'existe pas -> " + str(dto.id))
                    return JsonResponse(response.dict(),
                                        status=500)
                profil.updated_by = dto.updated_by
                profil.updated_at = dto.updated_at
                profil.is_deleted = dto.is_deleted if dto.is_deleted is not None else False
                profil.libelle = dto.libelle if dto.libelle is not None else profil.libelle

                # Sauvegardez le profil
                profil.save()

                # Ajouter un ProfilDto à la liste en excluant les champs avec des valeurs None
                items.append(ProfilDto(
                    id=profil.id,
                    code=profil.code,
                    libelle=profil.libelle,
                    is_deleted=profil.is_deleted,
                    created_by=profil.created_by,
                    updated_by=profil.updated_by,
                    updated_at=profil.updated_at,
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
            print("--------------- End update profil -----------------------")
            return JsonResponse(response.dict(), status=200)  # Utilisez JsonResponse pour retourner un objet JSON

        response.has_error = True
        response.status = Status(code=500, message="Liste de datas vide")
        return JsonResponse(response.dict(), status=500)

    @csrf_exempt
    @action(detail=False, methods=['delete'], url_name='delete')
    def delete(self, request, *args, **kwargs):
        print("--------------- Begin delete profil -----------------------")
        response = Response[ProfilDto]()
        json_data = request.body.decode('utf-8')
        request_data = json.loads(json_data)
        dtos = request_data.get('datas', [])
        items = []
        for dto_data in dtos:
            serializer = ProfilDtoSerializerToUpdate(data=dto_data)
            if serializer.is_valid():
                dto = serializer.create_profil_dto(serializer.validated_data)
                if dto.id is None:
                    response.has_error = True
                    response.status = Status(code=500, message="Champ id obligatoire")
                    return JsonResponse(response.dict(),
                                        status=500)

                existing_profil = Profil.objects.filter(id=dto.id).first()
                if existing_profil is None:
                    response.has_error = True
                    response.status = Status(code=500, message="Ce profil n'existe pas id -> " + str(dto.id))
                    return JsonResponse(response.dict(),
                                        status=500)

                dto.updated_at = str(timezone.now())
                dto.updated_by = 1

                existing_profil.updated_by = dto.updated_by
                existing_profil.updated_at = dto.updated_at
                existing_profil.is_deleted = True

                # Sauvegardez le profil
                existing_profil.save()

                # Ajouter un ProfilDto à la liste en excluant les champs avec des valeurs None
                items.append(ProfilDto(
                    id=existing_profil.id,
                    code=existing_profil.code,
                    libelle=existing_profil.libelle,
                    is_deleted=existing_profil.is_deleted,
                    created_by=existing_profil.created_by,
                    updated_by=existing_profil.updated_by,
                    updated_at=existing_profil.updated_at,
                    created_at=str(existing_profil.created_at),
                ))
            else:
                response.has_error = True
                response.status = Status(code=400, message="Validation de la requête a échoué")
                return JsonResponse(response.dict(), status=400)

        if items:
            response.has_error = False
            response.items = items
            response.count = len(items)
            print("--------------- End delete profil -----------------------")
            return JsonResponse(response.dict(), status=200)  # Utilisez JsonResponse pour retourner un objet JSON

        response.has_error = True
        response.status = Status(code=500, message="Liste de datas vide")
        return JsonResponse(response.dict(), status=500)

    @csrf_exempt
    @action(detail=False, methods=['get'], url_name='get_by_criteria')
    def get_by_criteria(self, request, *args, **kwargs):
        print("--------------- Begin get_by_criteria profil -----------------------")
        response = Response[ProfilDto]()
        json_data = request.body.decode('utf-8')
        request_data = json.loads(json_data)
        dtos = request_data.get('datas', [])
        items = []
        query = Q()
        for dto_data in dtos:

            serializer = ProfilDtoSerializerToGet(data=dto_data)
            if serializer.is_valid():
                dto = serializer.create_profil_dto(serializer.validated_data)
                if dto.libelle:
                    query &= Q(libelle=dto.libelle)
                if dto.id:
                    query &= Q(id=dto.id)
                if dto.code:
                    query &= Q(code=dto.code)
                if dto.is_deleted is not None:
                    query &= Q(is_deleted=dto.is_deleted)

                if dto.created_at:
                    try:
                        created_at_date = datetime.strptime(dto.created_at, "%d/%m/%Y")
                        query &= Q(updated_at=created_at_date)
                    except ValueError:
                        pass
                # Convertir la date au format "dd/mm/YYYY" en objet datetime
                if dto.updated_at:
                    try:
                        updated_at_date = datetime.strptime(dto.updated_at, "%d/%m/%Y")
                        query &= Q(created_at=updated_at_date)
                    except ValueError:
                        pass

                if dto.updated_by:
                    query &= Q(updated_by=dto.updated_by)
                if dto.deleted_by:
                    query &= Q(deleted_by=dto.deleted_by)
                if dto.created_by:
                    query &= Q(deleted_by=dto.created_by)

                profils = Profil.objects.filter(query)

                for profil in profils:
                    # Ajouter un ProfilDto à la liste en excluant les champs avec des valeurs None
                    items.append(ProfilDto(
                        id=profil.id,
                        code=profil.code,
                        libelle=profil.libelle,
                        is_deleted=profil.is_deleted,
                        created_by=profil.created_by,
                        updated_by=profil.updated_by,
                        updated_at=str(profil.updated_at),
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
            print("--------------- End get_by_criteria profil -----------------------")
            return JsonResponse(response.dict(), status=200)  # Utilisez JsonResponse pour retourner un objet JSON

        response.has_error = True
        response.status = Status(code=500, message="Liste de datas vide")
        return JsonResponse(response.dict(), status=500)


