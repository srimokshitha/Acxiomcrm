from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Customer(models.Model):
    customer_code = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=150, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, default='Active')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.customer_name

class Lead(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'), ('Contacted', 'Contacted'), 
        ('Qualified', 'Qualified'), ('Unqualified', 'Unqualified'), 
        ('Converted', 'Converted'), ('Lost', 'Lost')
    ]
    lead_code = models.CharField(max_length=50, unique=True)
    lead_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=150, blank=True)
    source = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    expected_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.lead_name

class Opportunity(models.Model):
    STAGE_CHOICES = [
        ('Qualification', 'Qualification'), ('Proposal', 'Proposal'),
        ('Negotiation', 'Negotiation'), ('Won', 'Won'), ('Lost', 'Lost')
    ]
    opportunity_name = models.CharField(max_length=150)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    stage = models.CharField(max_length=30, choices=STAGE_CHOICES, default='Qualification')
    probability = models.IntegerField(default=50)
    expected_close_date = models.DateField()
    status = models.CharField(max_length=20, default='Active')
    created_date = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if self.amount <= 0:
            raise ValidationError({'amount': 'Amount must be greater than 0.'})
        if self.probability < 0 or self.probability > 100:
            raise ValidationError({'probability': 'Probability must be between 0 and 100.'})
        if self.expected_close_date < timezone.now().date():
            raise ValidationError({'expected_close_date': 'Expected close date cannot be in the past.'})

class FollowUp(models.Model):
    TYPE_CHOICES = [('Call', 'Call'), ('Meeting', 'Meeting'), ('Email', 'Email'), ('Task', 'Task')]
    STATUS_CHOICES = [('Planned', 'Planned'), ('Completed', 'Completed'), ('Missed', 'Missed'), ('Cancelled', 'Cancelled')]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    follow_up_date = models.DateField()
    follow_up_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Call')
    remarks = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if self.status == 'Planned' and self.follow_up_date < timezone.now().date():
            raise ValidationError({'follow_up_date': 'Follow-up date cannot be earlier than today for planned follow-ups.'})

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50)
    entity_name = models.CharField(max_length=100)
    record_id = models.CharField(max_length=50, blank=True)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)