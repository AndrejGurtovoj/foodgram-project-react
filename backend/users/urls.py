from django.urls import include, path
from rest_framework import routers

from .views import SubscriptionView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'users/<user_id>/subscribe/',
        SubscriptionView.as_view(),
        name='subscriptions'
    ),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
