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



# in views.py
from django.db.models import Sum, Count
from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField
from .models import Status

# https://github.com/RamezIssac/django-slick-reporting

class TotalProductSales(ReportView):
    report_model = Status
    date_field = "created_at"
    group_by = "status"
    time_series_pattern = "daily"
    columns = [
        # "message_id",
        # "documentum_id",
        # "publication_id",
        # ComputationField.create(
        #     Sum, "quantity", verbose_name="Total quantity sold", is_summable=False
        # ),
        # ComputationField.create(
        #     Sum, "value", name="sum__value", verbose_name="Total Value sold $"
        # ),
        # ComputationField.create(Count, "message_id", name="count__message_id", verbose_name="Count")
    ]

    chart_settings = [
        # Chart(
        #     "Total sold $",
        #     Chart.BAR,
        #     data_source=["sum__value"],
        #     title_source=["name"],
        # ),
        # Chart(
        #     "Total sold $ [PIE]",
        #     Chart.PIE,
        #     data_source=["sum__value"],
        #     title_source=["name"],
        # ),
    ]
