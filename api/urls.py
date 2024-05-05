from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# Register StudentModelViewSet with Router
router.register('users', views.Users, basename='users')
# router.register('vendors/{vendor_id}/performance', views.HistoricalPerformanceModelViewSet, basename='performance')
router.register('vendors', views.VendorModelViewSet, basename='vendors')
router.register('purchase_orders', views.PurchaseOrderModelViewSet, basename='purchase_orders')


urlpatterns = [
    path('register/', views.register, name='register'),
    path('', include(router.urls)),
]