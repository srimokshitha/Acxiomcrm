from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crm.views import (
    CustomerViewSet, LeadViewSet, OpportunityViewSet,
    FollowUpViewSet, AuditLogViewSet
)

router = DefaultRouter()
router.register(r'api/customers', CustomerViewSet)
router.register(r'api/leads', LeadViewSet)
router.register(r'api/opportunities', OpportunityViewSet)
router.register(r'api/followups', FollowUpViewSet)
router.register(r'api/audit', AuditLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crm.views import (
    CustomerViewSet, LeadViewSet, OpportunityViewSet,
    FollowUpViewSet, AuditLogViewSet, dashboard
)

router = DefaultRouter()
router.register(r'api/customers', CustomerViewSet)
router.register(r'api/leads', LeadViewSet)
router.register(r'api/opportunities', OpportunityViewSet)
router.register(r'api/followups', FollowUpViewSet)
router.register(r'api/audit', AuditLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),
    path('', include(router.urls)),
]