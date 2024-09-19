from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('index.urls')),
    path('plataforma/', include('plataforma.urls')),
    path('plataforma/', include('amigos.urls')),
    path('plataforma/', include('perfil.urls'))

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
