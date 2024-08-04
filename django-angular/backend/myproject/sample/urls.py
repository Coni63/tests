from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AViewSet, BViewSet, CViewSet, TotalProductSales

router = DefaultRouter()
router.register(r'a', AViewSet)
router.register(r'b', BViewSet)
router.register(r'c', CViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("d", TotalProductSales.as_view())
]