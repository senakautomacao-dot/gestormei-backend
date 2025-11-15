import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .supabase_client import supabase


# =========================================================
# 🔥 Função auxiliar para validar autenticação Supabase
# =========================================================
def get_user_id(request):
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "").strip()

    try:
        user = supabase.auth.get_user(token)
        return user.user.id
    except Exception:
        return None


# =========================================================
# 📌 Rota: GET /api/receitas
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
# 📌 Rota: POST /api/add-receita
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
        descricao = body.get("descricao", "")
        valor = body.get("valor", 0)

        insert = (
            supabase.table("receitas")
            .insert({
                "user_id": user_id,
                "descricao": descricao,
                "valor": float(valor),
            })
            .execute()
        )

        return JsonResponse({"success": True, "data": insert.data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# =========================================================
# 📌 Rota: GET /api/compras
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
# 📌 Rota: POST /api/add-compra
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
        descricao = body.get("descricao", "")
        valor = body.get("valor", 0)

        insert = (
            supabase.table("compras")
            .insert({
                "user_id": user_id,
                "descricao": descricao,
                "valor": float(valor),
            })
            .execute()
        )

        return JsonResponse({"success": True, "data": insert.data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# =========================================================
# 📌 Rota: GET /api/dashboard (totalizadores)
# =========================================================
@csrf_exempt
def dashboard(request):
    user_id = get_user_id(request)
    if not user_id:
        return JsonResponse({"error": "Não autorizado"}, status=401)

    try:
        # Total Receitas
        rec = (
            supabase.table("receitas")
            .select("valor")
            .eq("user_id", user_id)
            .execute()
        )

        total_receitas = sum(item["valor"] for item in rec.data)

        # Total Compras
        comp = (
            supabase.table("compras")
            .select("valor")
            .eq("user_id", user_id)
            .execute()
        )

        total_compras = sum(item["valor"] for item in comp.data)

        return JsonResponse({
            "total_receitas": total_receitas,
            "total_compras": total_compras,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
