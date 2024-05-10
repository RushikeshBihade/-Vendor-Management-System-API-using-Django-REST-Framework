from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'vendors', VendorListView)
router.register(r'purchase_orders', PurchaseOrderListView)


urlpatterns = [
    path('',include(router.urls)),
    path('api/purchase_orders/<int:pk>/acknowledge/', PurchaseOrderListView.as_view({'post': 'acknowledge'}), name='acknowledge_purchase_order'),
    path('api/vendors/<int:pk>/performance/', VendorListView.as_view({'get': 'performance'}), name='vendor_performance'),
]
