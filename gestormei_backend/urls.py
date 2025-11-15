from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.urls import path
from .views import ReceitaCreate, ReceitaList, CompraCreate, CompraList, MeView

def status_view(request):
    return JsonResponse({"status": "online"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("status/", status_view),
    path("api/", include("core.urls")),
    path("receitas/", ReceitaCreate.as_view(), name="receita-create"),
    path("receitas/list/", ReceitaList.as_view(), name="receita-list"),
    path("compras/", CompraCreate.as_view(), name="compra-create"),
    path("compras/list/", CompraList.as_view(), name="compra-list"),
    path("me/", MeView.as_view(), name="me"),
]

