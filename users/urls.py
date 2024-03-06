from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from users import views
from users.views import LoginView, RegisterView, UserView, AddrView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('users/<int:pk>/', UserView.as_view({'get': 'retrieve'})),
    path('<int:pk>/avatar/upload/', UserView.as_view({'post': 'upload_avatar'})),
    path('address/', views.AddrView.as_view({"post": "create", "get": "list"})),
    path('address/', views.AddrView.as_view({"delete": "destroy", "put": "update"}))
]
