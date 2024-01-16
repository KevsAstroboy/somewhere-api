from django.utils.datetime_safe import datetime
from rest_framework import serializers

from ..utils.dto.user_dto import UserDto


class UserSerializerToSave(serializers.Serializer):
    nom = serializers.CharField(required=True)
    prenom = serializers.CharField(required=True)
    matricule = serializers.CharField(required=False)
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    contact = serializers.CharField(required=True)
    profil_id = serializers.IntegerField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    is_locked = serializers.BooleanField(required=False)
    is_super_admin = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    created_by = serializers.IntegerField(required=False)
    updated_by = serializers.IntegerField(required=False)
    deleted_by = serializers.IntegerField(required=False)

    def create_user_dto(self, validated_data):
        return UserDto(**validated_data)


class UserSerializerToUpdate(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    nom = serializers.CharField(required=False)
    prenom = serializers.CharField(required=False)
    matricule = serializers.CharField(required=False)
    login = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    contact = serializers.CharField(required=False)
    profil_id = serializers.IntegerField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    is_locked = serializers.BooleanField(required=False)

    def create_user_dto(self, validated_data):
        return UserDto(**validated_data)


class UserSerializerToGet(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    nom = serializers.CharField(required=False)
    prenom = serializers.CharField(required=False)
    matricule = serializers.CharField(required=False)
    login = serializers.CharField(required=False)
    contact = serializers.CharField(required=False)
    profil_id = serializers.IntegerField(required=False)
    profil_libelle = serializers.CharField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    is_locked = serializers.BooleanField(required=False)
    created_at = serializers.CharField(required=False)
    deleted_by = serializers.IntegerField(required=False)
    updated_at = serializers.CharField(required=False)
    created_by = serializers.IntegerField(required=False)
    updated_by = serializers.IntegerField(required=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Formater la date pour la représentation JSON
        if instance.created_at:
            ret['created_at'] = datetime.strftime(instance.created_at, '%d/%m/%Y %H:%M:%S')
        if instance.updated_at:
            ret['updated_at'] = datetime.strftime(instance.updated_at, '%d/%m/%Y %H:%M:%S')
        return ret

    def create_user_dto(self, validated_data):
        return UserDto(**validated_data)
