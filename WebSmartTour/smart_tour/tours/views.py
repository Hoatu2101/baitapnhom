from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets, generics, permissions, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from .models import (
    User, Role, Service,
    Booking, BookingTour, BookingHotel, BookingTransport,
    Invoice, Review
)
from .perms import IsProvider, IsCustomer
from .serializers import (
    UserSerializer, RoleSerializer, ServiceSerializer,
    BookingSerializer, BookingTourSerializer,
    BookingHotelSerializer, BookingTransportSerializer,
    InvoiceSerializer, ReviewSerializer
)
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import SupplierRegisterForm

# ================= ROLE =================
class RoleView(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# ================= USER =================
class UserView(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='current-user'
    )
    def current_user(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(UserSerializer(user).data)


# ================= SERVICE =================
class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [IsProvider]


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
        serializer.save(user=self.request.user)


# ================= BOOKING TOUR =================
class BookingTourView(viewsets.ModelViewSet):
    queryset = BookingTour.objects.all()
    serializer_class = BookingTourSerializer
    permission_classes = [permissions.IsAuthenticated]


# ================= BOOKING HOTEL =================
class BookingHotelView(viewsets.ModelViewSet):
    queryset = BookingHotel.objects.all()
    serializer_class = BookingHotelSerializer
    permission_classes = [permissions.IsAuthenticated]


# ================= BOOKING TRANSPORT =================
class BookingTransportView(viewsets.ModelViewSet):
    queryset = BookingTransport.objects.all()
    serializer_class = BookingTransportSerializer
    permission_classes = [permissions.IsAuthenticated]


# ================= INVOICE =================
class InvoiceView(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='revenue')
    def revenue_report(self, request):
        total = Invoice.objects.aggregate(total=models.Sum('total_amount'))
        return Response(total)

class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        service_id = self.request.query_params.get('service_id')
        qs = Review.objects.all()
        if service_id:
            qs = qs.filter(service_id=service_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



def register_supplier(request):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'avatar')

        error_messages = {
            'username': {
                'unique': "Tên đăng nhập này đã có người dùng. Vui lòng chọn tên khác nhé!",
            },
        }
    if request.method == 'POST':
        form = SupplierRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Đăng ký thành công! Vui lòng chờ Admin duyệt tài khoản.")
            return redirect('login')
    else:
        form = SupplierRegisterForm()

    return render(request, 'registration/register_supplier.html', {'form': form})
def intro_supplier(request):
    return render(request, 'intro_supplier.html')