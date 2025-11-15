from rest_framework import routers
from django.urls import path
from .views import ReceitaViewSet, CompraViewSet

router = routers.DefaultRouter()
router.register(r'receitas', ReceitaViewSet, basename='receita')
router.register(r'compras', CompraViewSet, basename='compra')

urlpatterns = router.urls
