from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (
    User, Role, Service,
    Booking, BookingTour, BookingHotel, BookingTransport,
    Invoice, Review, Payment
)

# ================= ROLE =================
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


# ================= USER =================
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password',
            'first_name', 'last_name',
            'email', 'avatar', 'role'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.avatar:
            data['avatar'] = instance.avatar.url
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        allowed = {'first_name', 'last_name', 'email', 'avatar'}
        if set(validated_data.keys()) - allowed:
            raise ValidationError("Chỉ được cập nhật thông tin cá nhân")
        return super().update(instance, validated_data)


# ================= SERVICE =================
class ServiceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    provider = serializers.StringRelatedField()

    class Meta:
        model = Service
        fields = [
            'id',
            'provider',
            'active',
            'created_date',
            'updated_date',
            'name',
            'description',
            'image',
            'price',
            'start_date',
            'available_slots',
            'service_type',
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class PaymentSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(),
        write_only=True,
        source='booking'
    )

    booking = serializers.PrimaryKeyRelatedField(read_only=True)
    method = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'booking',
            'booking_id',
            'method',
            'amount',
            'is_paid',
            'created_date'
        ]
        read_only_fields = (
            'booking',
            'method',
            'amount',
            'is_paid',
            'created_date'
        )

class PaymentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'method', 'amount', 'is_paid', 'created_date']


# ================= BOOKING =================
# class BookingSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     service = ServiceSerializer(read_only=True)
#     service_id = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(),
#         write_only=True,
#         source='service'
#     )
#
#     class Meta:
#         model = Booking
#         fields = '__all__'
#         read_only_fields = ('user', 'created_date')

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    payment = PaymentMiniSerializer(read_only=True)

    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        write_only=True,
        source='service'
    )

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user', 'created_date')



# ================= BOOKING TOUR =================
class BookingTourSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)

    class Meta:
        model = BookingTour
        fields = [
            'booking',
            'departure_date',
            'return_date',
            'transport',
            'hotel_name'
        ]


# ================= BOOKING HOTEL =================
class BookingHotelSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)

    class Meta:
        model = BookingHotel
        fields = [
            'booking',
            'hotel_name',
            'check_in',
            'check_out'
        ]


# ================= BOOKING TRANSPORT =================
class BookingTransportSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)

    class Meta:
        model = BookingTransport
        fields = [
            'booking',
            'transport_type',
            'departure_date'
        ]


# ================= INVOICE =================
class InvoiceSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_code',
            'booking',
            'payment_date',
            'total_amount'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        write_only=True,
        source='service'
    )

    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'created_date')

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        service = attrs.get('service')

        if not service:
            raise ValidationError({"service_id": "Thiếu service_id"})

        booking = Booking.objects.filter(
            user=user,
            service=service
        ).select_related('payment').first()

        if not booking:
            raise ValidationError("Bạn chưa đặt dịch vụ này")

        if not hasattr(booking, 'payment') or not booking.payment.is_paid:
            raise ValidationError("Bạn cần thanh toán trước khi bình luận")

        if Review.objects.filter(user=user, service=service).exists():
            raise ValidationError("Bạn đã đánh giá dịch vụ này rồi")

        return attrs


class ProviderServiceReportSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    service_name = serializers.CharField()
    total_bookings = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)


class TimeReportSerializer(serializers.Serializer):
    period = serializers.CharField()   # month / quarter / year
    total_bookings = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)


class AdminSummarySerializer(serializers.Serializer):
    total_services = serializers.IntegerField()
    total_bookings = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)