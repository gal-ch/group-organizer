from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import JointLoginSignupView, GroupCreate

urlpatterns = [
                  path('accounts/login/', JointLoginSignupView.as_view(), name='login'),
                  path('create-group/', GroupCreate.as_view(), name='create-group'),
                  path('', include('main.urls')),
                  path('', include('events.urls')),
                  path('accounts/', include('allauth.urls')),
                  url(r'^api-auth/', include('rest_framework.urls')),
                  path('admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
