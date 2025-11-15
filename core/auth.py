import os
import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from types import SimpleNamespace

SUPABASE_URL = os.getenv("SUPABASE_URL")


class SupabaseAuthentication(BaseAuthentication):
    """
    Valida o token JWT do Supabase chamando /auth/v1/user.
    """

    def authenticate(self, request):
        auth = request.headers.get("Authorization")

        if not auth:
            return None

        parts = auth.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise exceptions.AuthenticationFailed("Token Bearer inválido")

        token = parts[1]

        resp = requests.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={"Authorization": f"Bearer {token}"}
        )

        if resp.status_code != 200:
            raise exceptions.AuthenticationFailed("Token inválido")

        data = resp.json()

        user = SimpleNamespace(
            id=data.get("id"),
            email=data.get("email"),
            raw=data
        )

        return (user, token)
