from datetime import datetime

from rest_framework import serializers
from ..dao.entity.profil import Profil
from ..utils.dto.profil_dto import ProfilDto


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        exclude = ['updated_by', 'deleted_by', 'updated_at', 'code', 'created_at']


class ProfilDtoSerializerToSave(serializers.Serializer):
    libelle = serializers.CharField(required=True)

    def create_profil_dto(self, validated_data):
        return ProfilDto(**validated_data)
    # Ajoutez d'autres champs DTO si nécessaire


class ProfilDtoSerializerToUpdate(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    is_deleted = serializers.BooleanField(required=False)
    code = serializers.CharField(required=False)

    def create_profil_dto(self, validated_data):
        return ProfilDto(**validated_data)


class ProfilDtoSerializerToGet(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    code = serializers.CharField(required=False)
    created_at = serializers.CharField(required=False)
    deleted_by = serializers.IntegerField(required=False)
    libelle = serializers.CharField(required=False)
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

    def create_profil_dto(self, validated_data):
        return ProfilDto(**validated_data)
