from django.urls import path

from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(
    '',
    views.AccountViewSet,
    basename='accounts'
)

urlpatterns = [
    path('<int:pk>/change-password/',
         views.ChangePasswordView.as_view(),
         name='change-password'),
    path('login/', views.LoginView.as_view(), name='login'),
]

urlpatterns += router.urls
