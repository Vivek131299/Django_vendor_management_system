import datetime
import json

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Vendor, PurchaseOrder, HistoricalPerformance, POStatus
import random
import string
from rest_framework.decorators import action
from rest_framework.response import Response
from .signals import order_acknowledged_signal


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)

        username = request_body['username']
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists", status=409)
        email = request_body['email']

        # validate email
        try:
            validate_email(email)
        except ValidationError as e:
            print(e.message)
            return HttpResponse(f"Invalid email: {username}")

        password = request_body['password']

        User.objects.create_user(username=username, email=email, password=password)
        return HttpResponse(f"User created with username: {username}")


class Users(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class VendorModelViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        vendor_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        request.data['vendor_code'] = vendor_code
        return super().create(request, *args, **kwargs)

    # for url: GET /vendors/{id}/performance
    @action(detail=True, methods=['get'], url_path='performance')
    def vendor_performance(self, request, pk=None):
        if Vendor.objects.filter(pk=pk).exists():
            performance = HistoricalPerformance.objects.filter(vendor_id=pk).order_by('-date').first()
            serializer = HistoricalPerformanceSerializer(performance)
            return Response(serializer.data)
        else:
            return Response(f"No vendor with id {pk} exists.", status=404)


class PurchaseOrderModelViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if 'items' not in request.data:
            return Response("Field 'items' is required", status=400)
        if request.data['items'] is None or len(request.data['items']) == 0 or request.data['items'] == "":
            return Response("Field 'items' should contain at least one item", status=400)
        if 'vendor' not in request.data:
            return Response("Field 'vendor' is required", status=400)
        if request.data['vendor'] is None or request.data['vendor'] == "":
            return Response("Field 'vendor' should contain an integer", status=400)
        po_number = ''.join(random.choices(string.digits, k=10))
        order_date = datetime.date.today()
        request.data['order_date'] = order_date
        # calculating delivery_date of order by adding 7 days to order_date
        delivery_date = order_date + datetime.timedelta(days=7)
        request.data['po_number'] = po_number
        request.data['delivery_date'] = delivery_date
        request.data['quantity'] = len(request.data['items'])
        request.data['issue_date'] = datetime.datetime.now()
        return super().create(request, *args, **kwargs)

    # for url POST /purchase_orders/{id}/acknowledge/
    @action(detail=True, methods=['post'], url_path='acknowledge')
    def acknowledge_purchase_order(self, request, pk=None):
        purchase_order = self.get_object()
        if purchase_order.acknowledgment_date is not None:
            return Response(f"Purchase order has already been acknowledged on {datetime.datetime.strftime(purchase_order.acknowledgment_date, '%Y-%m-%d %H:%M:%S')}.")
        purchase_order.acknowledgment_date = datetime.datetime.now()
        purchase_order.save()
        order_acknowledged_signal.send(sender=PurchaseOrder, pk=pk)
        return Response("Purchase order acknowledged successfully.")

