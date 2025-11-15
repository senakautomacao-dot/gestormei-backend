import os
import requests
from rest_framework import authentication, exceptions
from types import SimpleNamespace

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Token inválido no header.')

        token = auth_header[1].decode()

        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            raise exceptions.AuthenticationFailed('Supabase não configurado.')

        url = f"{SUPABASE_URL}/auth/v1/user"
        headers = {
            'Authorization': f'Bearer {token}',
            'apikey': SUPABASE_ANON_KEY,
        }

        try:
            resp = requests.get(url, headers=headers, timeout=5)
        except Exception:
            raise exceptions.AuthenticationFailed('Falha ao conectar no Supabase.')

        if resp.status_code != 200:
            raise exceptions.AuthenticationFailed('Token inválido ou expirado.')

        data = resp.json()

        user_id = data.get('id') or data.get('sub') or data.get('user_id')
        if not user_id:
            raise exceptions.AuthenticationFailed('ID do usuário não encontrado.')

        user = SimpleNamespace()
        user.id = user_id
        user.email = data.get('email')
        user.is_authenticated = True

        return (user, None)
