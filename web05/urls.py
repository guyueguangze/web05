from django.contrib import admin
from django.urls import path, include, re_path

from users.views import FileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    re_path(r'file/image/(.+?)/', FileView.as_view())
]
