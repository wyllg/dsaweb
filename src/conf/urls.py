from django.contrib import admin
from django.urls import path, include
from conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'), name='home'),
    path('user/', include('django.contrib.auth.urls')),
    path('user/', include('user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
