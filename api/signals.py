
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save, pre_save
from .models import PurchaseOrder, POStatus, Vendor, HistoricalPerformance
import datetime


# Signal receiver for calculating on_time_delivery_rate, quality_rating_avg and fulfillment_rate
@receiver(pre_save, sender=PurchaseOrder)
def calculate_delivery_rate_quality_avg_fulfillment_rate(sender, instance, **kwargs):
    purchase_order = PurchaseOrder.objects.filter(pk=instance.id).first()

    fulfillment_rate = None
    new_on_time_delivery_rate = None
    new_quality_rating_avg = None

    # Getting latest historical performance record for the vendor
    old_historical_record = HistoricalPerformance.objects.filter(vendor_id=instance.vendor_id).order_by('-date').first()

    # FOR CALCULATING Fulfilment Rate
    total_orders = PurchaseOrder.objects.filter(vendor_id=instance.vendor_id).count()
    total_completed_orders = PurchaseOrder.objects.filter(vendor_id=instance.vendor_id, status=POStatus.COMPLETED.value).count()
    if instance.id is None:  # if new purchase order is being created
        if instance.status.lower() != POStatus.COMPLETED.value.lower():
            fulfillment_rate = total_completed_orders / (total_orders + 1)  # +1 for current order which will be saved after this pre_save()
        else:
            fulfillment_rate = (total_completed_orders + 1) / (total_orders + 1)
    else:
        if purchase_order.status.lower() != instance.status.lower():
            if instance.status.lower() == POStatus.COMPLETED.value.lower():  # if value is changed to Completed
                fulfillment_rate = (total_completed_orders + 1) / total_orders
            elif purchase_order.status.lower() == POStatus.COMPLETED.value.lower():  # if value changed from Completed to non-Completed
                fulfillment_rate = (total_completed_orders - 1) / total_orders

    if fulfillment_rate is not None:
        fulfillment_rate = round(fulfillment_rate * 100, 3)

    # FOR CALCULATING on_time_delivery_rate and quality_rating_avg
    if purchase_order:

        # Check if purchase order status is changed from non-Completed(Pending, etc.) to Completed
        if purchase_order.status != POStatus.COMPLETED.value and instance.status.lower() == POStatus.COMPLETED.value.lower():

            # FOR CALCULATING on_time_delivery_rate
            if datetime.date.today() <= purchase_order.order_date + datetime.timedelta(days=7):
                current_order_on_time = 1
            else:
                current_order_on_time = 0
            # Here, old calculated on_time_delivery_rate is used for calculating the new on_time_delivery_rate
            if old_historical_record and old_historical_record.on_time_delivery_rate is not None:
                old_on_time_delivery_rate = old_historical_record.on_time_delivery_rate
                total_completed_orders = PurchaseOrder.objects.filter(vendor_id=purchase_order.vendor_id, status=POStatus.COMPLETED.value).count()
                new_on_time_delivery_rate = (((old_on_time_delivery_rate / 100) * total_completed_orders) + current_order_on_time) / (total_completed_orders + 1)
                new_on_time_delivery_rate = round(new_on_time_delivery_rate * 100, 3)
            else:
                new_on_time_delivery_rate = current_order_on_time * 100

            # FOR CALCULATING quality_rating_avg:
            # if quality rating is provided for the current order
            if instance.quality_rating is not None:
                # Here as well, old calculated quality_rating_avg is used for calculating the new quality_rating_avg
                if old_historical_record and old_historical_record.quality_rating_avg is not None:
                    old_quality_rating_avg = old_historical_record.quality_rating_avg
                    total_orders_with_quality_rating = PurchaseOrder.objects.exclude(vendor_id=purchase_order.vendor_id, quality_rating__isnull=True).count()
                    new_quality_rating_avg = round(((old_quality_rating_avg * total_orders_with_quality_rating) + instance.quality_rating) / (total_orders_with_quality_rating + 1), 3)
                else:
                    new_quality_rating_avg = instance.quality_rating

    # get the current vendor for updating on_time_delivery_rate, quality_rating_avg and fulfillment_rate
    vendor = Vendor.objects.get(pk=instance.vendor_id)
    if new_on_time_delivery_rate is not None:
        vendor.on_time_delivery_rate = new_on_time_delivery_rate
    if new_quality_rating_avg is not None:
        vendor.quality_rating_avg = new_quality_rating_avg
    if fulfillment_rate is not None:
        vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

    # UPDATE/ADD on_time_delivery_rate, quality_rating_avg and fulfillment_rate into historical performance table.
    if old_historical_record:
        ''' Check if historical record was updated today. If so, update the same record with new value
             ensuring that the new performance record for a vendor is added only once per day.
             This is to avoid adding multiple new historical_performance records each time a
             purchase_order gets completed. We are adding a new record only once per day. Otherwise, we
             will just update the today's existing record with new values.'''
        if old_historical_record.date == datetime.date.today():
            if new_on_time_delivery_rate is not None:
                old_historical_record.on_time_delivery_rate = new_on_time_delivery_rate
            # update new calculated quality_rating_avg only if it is provided for current order
            if instance.quality_rating is not None:
                old_historical_record.quality_rating_avg = new_quality_rating_avg
            if fulfillment_rate is not None:
                old_historical_record.fulfillment_rate = fulfillment_rate
            old_historical_record.save()

        # If performance record for today doesn't exist, create a new one.
        else:
            # add new calculated quality_rating_avg if it is provided for current order or else keep the old one.
            if instance.quality_rating is not None:
                quality_rating_avg = new_quality_rating_avg
            else:
                quality_rating_avg = old_historical_record.quality_rating_avg

            if fulfillment_rate is None:
                fulfillment_rate = old_historical_record.fulfillment_rate

            if new_on_time_delivery_rate is None:
                new_on_time_delivery_rate = old_historical_record.on_time_delivery_rate

            new_historical_record = HistoricalPerformance.objects.create(
                vendor=old_historical_record.vendor,
                date=datetime.date.today(),
                on_time_delivery_rate=new_on_time_delivery_rate,
                quality_rating_avg=quality_rating_avg,
                average_response_time=old_historical_record.average_response_time,
                fulfillment_rate=fulfillment_rate
            )

    # If old record never existed for a vendor, create new. This case will occur when the vendor
    # completes its first order.
    else:
        if instance.quality_rating is not None:
            quality_rating_avg = new_quality_rating_avg
        else:
            quality_rating_avg = None

        new_historical_record = HistoricalPerformance.objects.create(
            vendor=vendor,
            date=datetime.date.today(),
            on_time_delivery_rate=new_on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            fulfillment_rate=fulfillment_rate
        )


# Custom signal for calculating average_response_time. To be triggered after purchase order is acknowledged.
order_acknowledged_signal = Signal()


@receiver(order_acknowledged_signal)
def calculate_average_response_time(sender, **kwargs):
    purchase_order = PurchaseOrder.objects.get(pk=kwargs['pk'])
    old_historical_record = HistoricalPerformance.objects.filter(vendor_id=purchase_order.vendor_id).order_by('-date').first()

    if old_historical_record and old_historical_record.average_response_time is not None:
        old_average_response_time = old_historical_record.average_response_time
        total_acknowledged_orders = PurchaseOrder.objects.exclude(vendor_id=purchase_order.vendor_id, acknowledgment_date__isnull=True).count()
        # calculate new average_response_time in hours (upto 3 decimal places)
        current_order_response_time = round((purchase_order.acknowledgment_date-purchase_order.issue_date).total_seconds() / 3600, 3)
        new_average_response_time = round(((old_average_response_time * (total_acknowledged_orders-1)) + current_order_response_time) / total_acknowledged_orders, 3)

    else:
        new_average_response_time = round((purchase_order.acknowledgment_date-purchase_order.issue_date).total_seconds() / 3600, 3)

    # update average_response_time for the vendor
    vendor = Vendor.objects.get(pk=purchase_order.vendor_id)
    vendor.average_response_time = new_average_response_time
    vendor.save()

    ''' Update/add average_response_time to Historical Performance record for the vendor
     We are here using the same logic as used above in calculate_delivery_rate_and_quality_avg function,
     i.e. we will add a new performance record only once per day, else we will update the existing for the same day.'''
    if old_historical_record:
        if old_historical_record.date == datetime.date.today():
            old_historical_record.average_response_time = new_average_response_time
            old_historical_record.save()
        else:
            new_historical_record = HistoricalPerformance.objects.create(
                vendor=old_historical_record.vendor,
                date=datetime.date.today(),
                on_time_delivery_rate=old_historical_record.on_time_delivery_rate,
                quality_rating_avg=old_historical_record.quality_rating_avg,
                average_response_time=new_average_response_time,
                fulfillment_rate=old_historical_record.fulfillment_rate
            )
    else:
        new_historical_record = HistoricalPerformance.objects.create(
            vendor=vendor,
            date=datetime.date.today(),
            average_response_time=new_average_response_time
        )
