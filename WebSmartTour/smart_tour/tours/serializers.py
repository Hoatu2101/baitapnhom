from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (
    User, Role, Service,
    Booking, BookingTour, BookingHotel, BookingTransport,
    Invoice, Review
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
    provider = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('provider', 'created_date', 'updated_date')



# ================= BOOKING =================
class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
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

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'created_date')

    def validate(self, data):
        user = self.context['request'].user
        service = data['service']
        if Review.objects.filter(user=user, service=service).exists():
            raise ValidationError("Đã đánh giá rồi")
        return data

