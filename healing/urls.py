from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
# para criar uma url dos arquivos de media
urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('medicos/', include('medico.urls')),
    path('pacientes/', include('paciente.urls')),
    path('', lambda request: redirect('/pacientes/home'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# static(qual vai ser a url - argumento 1, vai procurar aonde - argumento document_root)