from rest_framework import routers
from django.urls import path
from .views import ReceitaViewSet, CompraViewSet
from .views import ReceitaCreate, ReceitaList, CompraCreate, CompraList, MeView

router = routers.DefaultRouter()
router.register(r'receitas', ReceitaViewSet, basename='receita')
router.register(r'compras', CompraViewSet, basename='compra')

urlpatterns = router.urls

# core/urls.py

urlpatterns = [
    path("receitas/", ReceitaCreate.as_view(), name="receita-create"),
    path("receitas/list/", ReceitaList.as_view(), name="receita-list"),
    path("compras/", CompraCreate.as_view(), name="compra-create"),
    path("compras/list/", CompraList.as_view(), name="compra-list"),
    path("me/", MeView.as_view(), name="me"),
]
