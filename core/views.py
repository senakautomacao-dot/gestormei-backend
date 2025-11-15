from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from .models import Receita, Compra, Profile
from .serializers import ReceitaSerializer, CompraSerializer, ProfileSerializer

def get_user_id(request):
    return getattr(request.user, 'id', None)

class ReceitaViewSet(viewsets.ModelViewSet):
    serializer_class = ReceitaSerializer

    def get_queryset(self):
        user_id = get_user_id(self.request)
        return Receita.objects.filter(user_id=user_id).order_by('-created_at')

    def perform_create(self, serializer):
        user_id = get_user_id(self.request)
        serializer.save(user_id=user_id)

class CompraViewSet(viewsets.ModelViewSet):
    serializer_class = CompraSerializer

    def get_queryset(self):
        user_id = get_user_id(self.request)
        return Compra.objects.filter(user_id=user_id).order_by('-created_at')

    def perform_create(self, serializer):
        user_id = get_user_id(self.request)
        serializer.save(user_id=user_id)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = get_user_id(request)
        try:
            profile = Profile.objects.get(id=user_id)
            return Response(ProfileSerializer(profile).data)
        except Profile.DoesNotExist:
            return Response({'detail': 'Perfil não encontrado'}, status=404)

    def post(self, request):
        user_id = get_user_id(request)
        data = request.data.copy()
        data['id'] = user_id

        s = ProfileSerializer(data=data)
        if s.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO profiles (id, cnpj, razao_social, data_abertura)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE
                    SET cnpj = EXCLUDED.cnpj,
                        razao_social = EXCLUDED.razao_social,
                        data_abertura = EXCLUDED.data_abertura
                """, [
                    user_id,
                    s.validated_data.get('cnpj'),
                    s.validated_data.get('razao_social'),
                    s.validated_data.get('data_abertura'),
                ])
            return Response({"detail": "Perfil salvo com sucesso"})
        return Response(s.errors, status=400)
