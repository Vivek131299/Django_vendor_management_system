import datetime

from django.db import models
from enum import Enum


class POStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELED = "Canceled"


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField(max_length=100)
    address = models.TextField(max_length=100)
    vendor_code = models.CharField(max_length=10)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=10, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True)
    order_date = models.DateField(blank=True)
    delivery_date = models.DateField(blank=True)
    items = models.JSONField(blank=True)
    quantity = models.IntegerField(blank=True)
    status = models.CharField(max_length=20, default=POStatus.PENDING.value, blank=True)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(blank=True)
    acknowledgment_date = models.DateTimeField(null=True)


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateField()
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

