from rest_framework import serializers
from .models import AccessibilityForm

class AccessibilityFormSerializers(serializers.ModelSerializer):
    class Meta:
        model = AccessibilityForm
        fields = '__all__'
        read_only_fields = ['user','branch']