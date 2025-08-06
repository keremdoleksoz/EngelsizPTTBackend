from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccessibilityFormViewSet

router = DefaultRouter()
router.register(r'forms', AccessibilityFormViewSet, basename='form')

urlpatterns = [
    path('', include(router.urls)),
]
