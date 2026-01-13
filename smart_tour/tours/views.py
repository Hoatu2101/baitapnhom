from django.contrib import messages
from django.db.models import Count, Sum
from django.db.models.functions import TruncYear, TruncMonth
from django.shortcuts import redirect, render
from rest_framework import viewsets, permissions, parsers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .perms import IsProvider, IsCustomer, IsOwner, ReadOnly
from .form import SupplierRegisterForm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .throttles import ProviderRateThrottle

from .models import (
    Service, Booking, Review, Payment, Role, BookingTour, BookingHotel, BookingTransport, Invoice
)
from .serializers import (
    ServiceSerializer,
    BookingSerializer,
    ReviewSerializer,
    PaymentSerializer, RoleSerializer, UserSerializer, BookingTourSerializer, BookingHotelSerializer,
    BookingTransportSerializer, InvoiceSerializer,
)

# ================= ROLE =================
class RoleView(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# ================= USER =================
class UserView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(methods=['get', 'patch'], detail=False, url_path='me')
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(UserSerializer(user).data)


# ================= SERVICE =================
class ServiceView(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    throttle_classes = [ProviderRateThrottle]

    def get_queryset(self):
        qs = Service.objects.filter(active=True)
        user = self.request.user

        if user.is_authenticated and user.role and user.role.name == 'PROVIDER':
            return qs.filter(provider=user)

        return qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsProvider()]

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

    @action(detail=False, methods=['get'], url_path='compare')
    def compare(self, request):
        ids = request.query_params.get('ids')
        service_type = request.query_params.get('type')

        qs = Service.objects.filter(active=True)

        if ids:
            qs = qs.filter(id__in=ids.split(','))
        if service_type:
            qs = qs.filter(service_type=service_type)

        return Response(ServiceSerializer(qs, many=True).data)


# ================= BOOKING =================
class BookingView(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        service = booking.service

        if service.available_slots is not None:
            if service.available_slots <= 0:
                raise ValidationError("Dịch vụ đã hết chỗ")
            service.available_slots -= 1
            service.save()


# ================= BOOKING DETAIL =================
class BookingTourView(viewsets.ModelViewSet):
    queryset = BookingTour.objects.all()
    serializer_class = BookingTourSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookingHotelView(viewsets.ModelViewSet):
    queryset = BookingHotel.objects.all()
    serializer_class = BookingHotelSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookingTransportView(viewsets.ModelViewSet):
    queryset = BookingTransport.objects.all()
    serializer_class = BookingTransportSerializer
    permission_classes = [permissions.IsAuthenticated]


# ================= PAYMENT =================
class PaymentView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Payment.objects.filter(booking__user=self.request.user)

    def perform_create(self, serializer):
        booking = serializer.validated_data['booking']

        if booking.user != self.request.user:
            raise ValidationError("Không thể thanh toán booking của người khác")

        serializer.save(
            amount=booking.service.price,
            is_paid=True
        )


# ================= INVOICE =================
class InvoiceView(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Invoice.objects.all()
        return Invoice.objects.filter(booking__user=user)


# ================= REVIEW =================
class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    throttle_classes = [ProviderRateThrottle]

    def get_queryset(self):
        qs = Review.objects.filter(active=True)
        service_id = self.request.query_params.get('service_id')
        if service_id:
            qs = qs.filter(service_id=service_id)
        return qs

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [IsCustomer()]
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         return [IsOwner()]
    #     return [ReadOnly()]
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'create':
            return [IsCustomer()]
        return [IsOwner()]

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# ================= REPORT =================
class ProviderReportView(APIView):
    permission_classes = [IsProvider]
    throttle_classes = [ProviderRateThrottle]

    @swagger_auto_schema(
        tags=['Reports - Provider'],
        operation_summary="Báo cáo doanh thu nhà cung cấp",
        manual_parameters=[
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="month | quarter | year",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        period = request.query_params.get('period', 'month')

        qs = Payment.objects.filter(
            booking__service__provider=request.user,
            is_paid=True
        )

        from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear

        if period == 'year':
            qs = qs.annotate(p=TruncYear('created_date'))
        elif period == 'quarter':
            qs = qs.annotate(p=TruncQuarter('created_date'))
        else:
            qs = qs.annotate(p=TruncMonth('created_date'))

        data = qs.values('p').annotate(
            total_bookings=openapi.models.Count('id'),
            total_revenue=openapi.models.Sum('amount')
        ).order_by('p')

        return Response(data)



class AdminReportView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response({
            "total_services": Service.objects.filter(active=True).count(),
            "total_bookings": Booking.objects.count(),
            "total_revenue": Payment.objects.filter(is_paid=True)
                .aggregate(total=Sum('amount'))['total']
        })

class ProviderServiceReportView(APIView):
    permission_classes = [IsProvider]

    def get(self, request):
        qs = Service.objects.filter(
            provider=request.user
        ).annotate(
            total_bookings=Count('booking'),
            total_revenue=Sum('booking__payment__amount')
        )

        data = [
            {
                'service_id': s.id,
                'service_name': s.name,
                'total_bookings': s.total_bookings or 0,
                'total_revenue': s.total_revenue or 0
            }
            for s in qs
        ]

        return Response(data)

class ProviderTimeReportView(APIView):
    permission_classes = [IsProvider]

    def get(self, request):
        period = request.query_params.get('period', 'month')

        qs = Payment.objects.filter(
            booking__service__provider=request.user,
            is_paid=True
        )

        if period == 'year':
            qs = qs.annotate(p=TruncYear('created_date'))
        else:
            qs = qs.annotate(p=TruncMonth('created_date'))

        data = qs.values('p').annotate(
            total_bookings=Count('id'),
            total_revenue=Sum('amount')
        ).order_by('p')

        return Response([
            {
                'period': str(i['p'].date()),
                'total_bookings': i['total_bookings'],
                'total_revenue': i['total_revenue']
            }
            for i in data
        ])


def register_supplier(request):
    """
    Trang đăng ký nhà cung cấp (HTML FORM)
    """
    if request.method == 'POST':
        form = SupplierRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)

            try:
                supplier_role = Role.objects.get(name='PROVIDER')
                user.role = supplier_role
            except Role.DoesNotExist:
                messages.error(request, "Role PROVIDER chưa tồn tại")
                return redirect('register_supplier')

            user.is_verified = False
            user.save()

            messages.success(
                request,
                "Đăng ký thành công! Vui lòng chờ Admin duyệt tài khoản."
            )
            return redirect('login')
    else:
        form = SupplierRegisterForm()

    return render(request, 'registration/register_supplier.html', {'form': form})


def intro_supplier(request):
    return render(request, 'intro_supplier.html')
