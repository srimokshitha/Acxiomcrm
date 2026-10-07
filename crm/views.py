from django.shortcuts import render
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Customer, Lead, Opportunity, FollowUp, AuditLog
from .serializers import (
    CustomerSerializer, LeadSerializer, OpportunitySerializer,
    FollowUpSerializer, AuditLogSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FollowUpViewSet(viewsets.ModelViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

def dashboard(request):
    total_customers = Customer.objects.count()
    total_leads = Lead.objects.count()
    open_leads = Lead.objects.exclude(status__in=['Converted', 'Lost']).count()
    total_opportunities = Opportunity.objects.count()
    open_opportunities = Opportunity.objects.filter(status='Active').count()
    won_opportunities = Opportunity.objects.filter(stage='Won').count()
    lost_opportunities = Opportunity.objects.filter(stage='Lost').count()
    total_pipeline = Opportunity.objects.filter(status='Active').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'total_customers': total_customers,
        'total_leads': total_leads,
        'open_leads': open_leads,
        'total_opportunities': total_opportunities,
        'open_opportunities': open_opportunities,
        'won_opportunities': won_opportunities,
        'lost_opportunities': lost_opportunities,
        'total_pipeline': total_pipeline,
    }
    return render(request, 'crm/dashboard.html', context)