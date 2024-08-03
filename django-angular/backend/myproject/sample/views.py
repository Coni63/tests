from django.shortcuts import render
from rest_framework import viewsets
from .models import A, B, C
from .serializer import ASerializer, BSerializer, CSerializer

# Create your views here.

class AViewSet(viewsets.ModelViewSet):
    queryset = A.objects.all()
    serializer_class = ASerializer

class BViewSet(viewsets.ModelViewSet):
    queryset = B.objects.all()
    serializer_class = BSerializer

class CViewSet(viewsets.ModelViewSet):
    queryset = C.objects.all()
    serializer_class = CSerializer