from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path ('api/', include('accounts.urls')),
    path ('auth/', include('djoser.urls')),
    path ('auth/', include('djoser.urls.jwt')),
    path ('api/', include('exams.urls')),
    path ('api/', include('pacients.urls')),
    path ('api/', include('endoscopies.urls')),
    path ('api/', include('als.urls')),
    path ('api/', include('unlabeled.urls')),
    path ('api/', include('training.urls')),
    path ('api/', include('testing.urls')),
    path ('api/', include('anotations.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]

# Site Admin - http://127.0.0.1:8000/admin/

# Registar Users - http://127.0.0.1:8000/auth/users/
# Confirmar Conta - http://127.0.0.1:8000/auth/users/activation/
# Get JSON Web Token - http://127.0.0.1:8000/auth/jwt/create/
    # "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNzcwNjQ1NywianRpIjoiNzZlNjFmMDIwYjZlNDk0NGJlOTI2ZDQ0YzFjNzBhMWQiLCJ1c2VyX2lkIjoxfQ.8nyuqYVIPN7NbOBqZOryazGfNmNF-XRnUxEPRVaJYEo",
    #"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE3NjIwMzU3LCJqdGkiOiI3NWFhY2JjYTI0NmU0NzlhYTMxN2NhZDU2NzM1YmQwZSIsInVzZXJfaWQiOjF9.AzAW0tlYq2_YW1X8pLBXSnmpxe-4WAmw8mP2YgYN_0U"
# Get New Access Token - http://127.0.0.1:8000/auth/jwt/refresh/
# Reset Password - http://127.0.0.1:8000/auth/users/reset_password/
# Confirmar Password - http://127.0.0.1:8000/auth/users/reset_password_confirm/

# Registar/Alterar/Apagar/... Exames - http://127.0.0.1:8000/api/exams/<id>/
# Registar/Alterar/Apagar/... Pacientes- http://127.0.0.1:8000/api/pacients/<id>/
# Registar//Apagar/... Endoscopias- http://127.0.0.1:8000/api/endoscopies/<id>/
# Registar/Alterar/Apagar/... Active Learning- http://127.0.0.1:8000/api/als/<id>/
# Ativar Active Learning- http://127.0.0.1:8000/api/als/activated/<id>/ sem id obtem o AL ativado e com id ativa esse o AL com esse id

