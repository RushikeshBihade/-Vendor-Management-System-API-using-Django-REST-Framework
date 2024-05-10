from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count, Avg
from django.db.models import F
from django.utils import timezone

# Create vendor models.
class Vendor(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True, primary_key=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    averae_response_time = models.FloatField(default=0)
    fulfilment_rate = models.FloatField(default=0)

    def update_performance_metrics(self):
        # update on_time_delivery_rate
        completed_pos = self.purchase_orders.filter(status='completed')
        total_completed_pos = completed_pos.count()
        on_time_deliveries = completed_pos.filter(delivery_date__lte=models.F('acknowledgment_date')).count()
        self.on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100 if total_completed_pos > 0 else 0
        
        # update quality_rating_average
        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        self.quality_rating_avg = completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
        
        # update  average_response_time
        acknowledged_pos = completed_pos.exclude(acknowledgment_date=None)
        response_times = acknowledged_pos.annotate(response_time=models.F('acknowledgment_date') - models.F('issue_date'))
        self.average_response_time = response_times.aggregate(Avg('response_time'))['response_time__avg'].total_seconds() or 0
        
        # update fulfillment_rate
        total_pos = self.purchase_orders.all()
        successfully_fulfilled_pos = completed_pos.exclude(issue_date=None)
        self.fulfillment_rate = (successfully_fulfilled_pos.count() / total_pos.count()) * 100 if total_pos.count() > 0 else 0

        self.save()

# create PurchaseOrder model    
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.PositiveIntegerField()
    delivered_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'completed':
            self.vendor.update_performance_metrics()

        if self.status == 'completed' and self.vendor_id is not None:
            self.vendor.update_performance_metrics()

# create Performance Model
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()    

