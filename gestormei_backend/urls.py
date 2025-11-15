from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def status_view(request):
    return JsonResponse({"status": "online"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("status/", status_view),
    path("api/", include("core.urls")),
]
