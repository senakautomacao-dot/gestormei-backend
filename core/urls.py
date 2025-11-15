from django.urls import path
from .views import (
    ReceitasView,
    ComprasView,
    add_receita,
    add_compra,
    dashboard,
)

urlpatterns = [
    # =============================
    # 📌 Receitas
    # =============================
    path("receitas/", ReceitasView.as_view(), name="listar_receitas"),
    path("add-receita/", add_receita, name="add_receita"),

    # =============================
    # 📌 Compras
    # =============================
    path("compras/", ComprasView.as_view(), name="listar_compras"),
    path("add-compra/", add_compra, name="add_compra"),

    # =============================
    # 📊 Dashboard
    # =============================
    path("dashboard/", dashboard, name="dashboard"),
]
