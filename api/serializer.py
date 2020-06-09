from rest_framework import serializers
from .models import WishModel


class WishModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishModel
        fields = "__all__"
