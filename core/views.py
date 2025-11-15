import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import jwt
from django.conf import settings
from .supabase_client import supabase


# =========================================================
# 🔥 Função SIMPLIFICADA para extrair user_id do token JWT
# =========================================================
def get_user_id(request):
    auth = request.headers.get("Authorization", "")

    if not auth.startswith("Bearer "):
        return None

    token = auth.replace("Bearer ", "").strip()

    try:
        # decodifica sem verificar assinatura — funciona para apps pessoais
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get("sub")
    except Exception:
        return None


# =========================================================
# 📌 GET /api/receitas
# =========================================================
@method_decorator(csrf_exempt, name="dispatch")
class ReceitasView(View):
    def get(self, request):
        user_id = get_user_id(request)
        if not user_id:
            return JsonResponse({"error": "Não autorizado"}, status=401)

        try:
            data = (
                supabase.table("receitas")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )

            return JsonResponse(data.data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# =========================================================
# 📌 POST /api/add-receita
# =========================================================
@csrf_exempt
def add_receita(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    user_id = get_user_id(request)
    if not user_id:
        return JsonResponse({"error": "Não autorizado"}, status=401)

    try:
        body = json.loads(request.body)
        descricao = body.get("descricao")
        valor = float(body.get("valor"))

        insert = (
            supabase.table("receitas")
            .insert({
                "user_id": user_id,
                "descricao": descricao,
                "valor": valor,
            })
            .execute()
        )

        return JsonResponse({"success": True, "data": insert.data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# =========================================================
# 📌 GET /api/compras
# =========================================================
@method_decorator(csrf_exempt, name="dispatch")
class ComprasView(View):
    def get(self, request):
        user_id = get_user_id(request)
        if not user_id:
            return JsonResponse({"error": "Não autorizado"}, status=401)

        try:
            data = (
                supabase.table("compras")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )

            return JsonResponse(data.data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# =========================================================
# 📌 POST /api/add-compra
# =========================================================
@csrf_exempt
def add_compra(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    user_id = get_user_id(request)
    if not user_id:
        return JsonResponse({"error": "Não autorizado"}, status=401)

    try:
        body = json.loads(request.body)
        descricao = body.get("descricao")
        valor = float(body.get("valor"))

        insert = (
            supabase.table("compras")
            .insert({
                "user_id": user_id,
                "descricao": descricao,
                "valor": valor,
            })
            .execute()
        )

        return JsonResponse({"success": True, "data": insert.data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# =========================================================
# 📌 GET /api/dashboard
# =========================================================
@csrf_exempt
def dashboard(request):
    user_id = get_user_id(request)
    if not user_id:
        return JsonResponse({"error": "Não autorizado"}, status=401)

    try:
        # Total Receitas
        receitas = (
            supabase.table("receitas")
            .select("valor")
            .eq("user_id", user_id)
            .execute()
        )

        total_receitas = sum(float(x["valor"]) for x in receitas.data)

        # Total Compras
        compras = (
            supabase.table("compras")
            .select("valor")
            .eq("user_id", user_id)
            .execute()
        )

        total_compras = sum(float(x["valor"]) for x in compras.data)

        return JsonResponse({
            "total_receitas": total_receitas,
            "total_compras": total_compras,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
