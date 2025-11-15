from rest_framework import routers
from .views import ReceitaViewSet, CompraViewSet, ProfileView
from django.urls import path

router = routers.DefaultRouter()
router.register(r'receitas', ReceitaViewSet, basename='receita')
router.register(r'compras', CompraViewSet, basename='compra')

urlpatterns = router.urls + [
    path('profile/', ProfileView.as_view(), name='profile'),
]
