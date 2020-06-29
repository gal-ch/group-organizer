from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('', include('main.urls')),
                  path('', include('events.urls')),
                  path('', include('accounts.urls')),
                  path('accounts/', include('allauth.urls')),
                  url(r'^api-auth/', include('rest_framework.urls')),
                  path('admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
