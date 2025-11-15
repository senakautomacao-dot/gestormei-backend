from rest_framework import serializers
from .models import Receita, Compra, Profile

class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ['id','descricao','valor','created_at']

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['id','descricao','valor','created_at']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','cnpj','razao_social','data_abertura']
