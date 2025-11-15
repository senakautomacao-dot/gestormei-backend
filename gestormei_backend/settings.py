import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# 🔐 Configurações de Segurança
# ================================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "*", 
    "gestor-mei-backend.onrender.com",
]


# ================================
# 📦 Apps Instalados
# ================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Libs
    'rest_framework',
    'corsheaders',

    # App principal
    'core',
]


# ================================
# 🧱 Middleware
# ================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


# ================================
# 🌍 CORS (Liberação para Frontend)
# ================================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-supabase-auth",
]

CORS_EXPOSE_HEADERS = [
    "authorization",
    "x-supabase-auth",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]


# ================================
# 🛡 CSRF (Confiança nas Origens)
# ================================
CSRF_TRUSTED_ORIGINS = [
    "https://gestor-mei-backend.onrender.com",
    "https://gestor-mei-front.onrender.com",  # 👈 MUITO IMPORTANTE
    "https://zrpxtooampraytmkywhl.supabase.co",
    "http://localhost:3000",
    "http://localhost:8000",
]


# ================================
# 🌐 URLs e WSGI
# ================================
ROOT_URLCONF = 'gestormei_backend.urls'
WSGI_APPLICATION = 'gestormei_backend.wsgi.application'


# ================================
# 🗄 Banco de Dados: Supabase
# ================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PG_DB', 'postgres'),
        'USER': os.environ.get('PG_USER', 'postgres'),
        'PASSWORD': os.environ.get('PG_PASS', ''),
        'HOST': os.environ.get('PG_HOST', ''),
        'PORT': os.environ.get('PG_PORT', '5432'),
    }
}


# ================================
# 📁 Arquivos Estáticos
# ================================
STATIC_URL = '/static/'


# ================================
# 🔑 REST Framework (Autenticação)
# ================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "core.auth.SupabaseAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}


# ================================
# 🔌 Configuração Supabase
# ================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE = os.environ.get("SUPABASE_SERVICE_ROLE", "")
