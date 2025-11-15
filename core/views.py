from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .supabase_client import supabase


class MeView(APIView):
    """
    Retorna o usuário autenticado + perfil (tabela profiles)
    """
    def get(self, request):
        user = request.user

        if not user or not getattr(user, "id", None):
            return Response({"detail": "Não autenticado"}, status=401)

        profile = supabase.table("profiles") \
            .select("*") \
            .eq("id", user.id) \
            .single() \
            .execute()

        return Response({
            "user": {"id": user.id, "email": user.email},
            "profile": profile.data
        })


class ReceitaCreate(APIView):
    """
    Cria receita no Supabase
    """
    def post(self, request):
        user = request.user
        if not user or not getattr(user, "id", None):
            return Response({"detail": "Não autenticado"}, status=401)

        descricao = request.data.get("descricao")
        valor = request.data.get("valor")

        if not descricao or valor is None:
            return Response({"detail": "descricao e valor obrigatórios"}, status=400)

        data = {
            "user_id": user.id,
            "descricao": descricao,
            "valor": valor
        }

        result = supabase.table("receitas").insert(data).execute()

        if result.error:
            return Response({"detail": str(result.error)}, status=500)

        return Response(result.data, status=201)


class ReceitaList(APIView):
    """
    Lista receitas do usuário autenticado
    """
    def get(self, request):
        user = request.user

        result = supabase.table("receitas") \
            .select("*") \
            .eq("user_id", user.id) \
            .order("created_at", desc=True) \
            .execute()

        return Response(result.data or [])


class CompraCreate(APIView):
    """
    Cria compra no Supabase
    """
    def post(self, request):
        user = request.user
        if not user:
            return Response({"detail": "Não autenticado"}, status=401)

        descricao = request.data.get("descricao")
        valor = request.data.get("valor")

        if not descricao or valor is None:
            return Response({"detail": "descricao e valor obrigatórios"}, status=400)

        data = {
            "user_id": user.id,
            "descricao": descricao,
            "valor": valor
        }

        result = supabase.table("compras").insert(data).execute()

        if result.error:
            return Response({"detail": str(result.error)}, status=500)

        return Response(result.data, status=201)


class CompraList(APIView):
    """
    Lista compras do usuário autenticado
    """
    def get(self, request):
        user = request.user

        result = supabase.table("compras") \
            .select("*") \
            .eq("user_id", user.id) \
            .order("created_at", desc=True) \
            .execute()

        return Response(result.data or [])
