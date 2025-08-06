from rest_framework import viewsets
from .models import AccessibilityForm
from .serializers import AccessibilityFormSerializers
from rest_framework.permissions import IsAuthenticated

class AccessibilityFormViewSet(viewsets.ModelViewSet):
    queeryset= AccessibilityForm.objects.all()
    serializer_class = AccessibilityFormSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            branch =self.request.user.branch)