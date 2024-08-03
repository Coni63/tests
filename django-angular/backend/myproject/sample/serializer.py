from rest_framework import serializers
from .models import A, B, C, AtoB

class BSerializer(serializers.ModelSerializer):
    class Meta:
        model = B
        fields = ['id', 'title']


class CSerializer(serializers.ModelSerializer):
    class Meta:
        model = C
        fields = ['id', 'category']

class AtoBSerializer(serializers.ModelSerializer):
    b = BSerializer(read_only=True)

    class Meta:
        model = AtoB
        fields = ['b', 'order']

class ASerializer(serializers.ModelSerializer):
    bs = serializers.SerializerMethodField()

    class Meta:
        model = A
        fields = ['id', 'name', 'bs', 'category']

    def get_bs(self, obj):
        atob = AtoB.objects.filter(a=obj).order_by('order')
        return AtoBSerializer(atob, many=True).data