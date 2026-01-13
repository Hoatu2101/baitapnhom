from django.utils import timezone
from datetime import timedelta, date
from accounts.models import User, Role
from services.models import Service, Booking, BookingTour, BookingHotel, BookingTransport, Review, Payment, Invoice


customer_role, _ = Role.objects.get_or_create(name="CUSTOMER")
provider_role, _ = Role.objects.get_or_create(name="PROVIDER")

provider, _ = User.objects.get_or_create(
    username="provider1",
    email="provider1@example.com",
    defaults={
        "role": provider_role,
        "is_verified": True
    }
)
provider.set_password("Provider@123")
provider.save()

customer, _ = User.objects.get_or_create(
    username="customer1",
    email="customer1@example.com",
    defaults={
        "role": customer_role,
        "is_verified": True
    }
)
customer.set_password("Customer@123")
customer.save()

# =========================
# 3. SERVICES (do PROVIDER tạo)
# =========================
tour = Service.objects.create(
    name="Hà Nội – Hạ Long 3N2Đ",
    description="Tour du lịch Hạ Long cao cấp",
    price=3500000,
    start_date=timezone.now() + timedelta(days=7),
    available_slots=20,
    service_type="TOUR",
    provider=provider
)

hotel = Service.objects.create(
    name="Khách sạn 5 sao Đà Nẵng",
    description="Khách sạn ven biển",
    price=1800000,
    start_date=timezone.now() + timedelta(days=5),
    available_slots=10,
    service_type="HOTEL",
    provider=provider
)

transport = Service.objects.create(
    name="Xe limousine Sài Gòn – Đà Lạt",
    description="Xe limousine cao cấp",
    price=450000,
    start_date=timezone.now() + timedelta(days=3),
    available_slots=15,
    service_type="TRANSPORT",
    provider=provider
)


booking_tour = Booking.objects.create(
    user=customer,
    service=tour,
    booking_date=timezone.now(),
    description="Đặt tour cho gia đình"
)

BookingTour.objects.create(
    booking=booking_tour,
    departure_date=date.today() + timedelta(days=7),
    return_date=date.today() + timedelta(days=9),
    transport="Xe du lịch",
    hotel_name="Vinpearl Hạ Long"
)

booking_hotel = Booking.objects.create(
    user=customer,
    service=hotel,
    booking_date=timezone.now()
)

BookingHotel.objects.create(
    booking=booking_hotel,
    hotel_name="InterContinental Đà Nẵng",
    check_in=date.today() + timedelta(days=5),
    check_out=date.today() + timedelta(days=7)
)

booking_transport = Booking.objects.create(
    user=customer,
    service=transport,
    booking_date=timezone.now()
)

BookingTransport.objects.create(
    booking=booking_transport,
    transport_type="Limousine",
    departure_date=date.today() + timedelta(days=3)
)

# =========================
# 5. PAYMENT
# =========================
Payment.objects.create(
    booking=booking_tour,
    method="MOMO",
    amount=tour.price,
    is_paid=True,
    transaction_id="MOMO123456"
)

# =========================
# 6. INVOICE
# =========================
Invoice.objects.create(
    invoice_code="INV-001",
    booking=booking_tour,
    payment_date=timezone.now(),
    total_amount=tour.price
)

# =========================
# 7. REVIEW
# =========================
Review.objects.create(
    user=customer,
    service=tour,
    rating=5,
    comment="Dịch vụ rất tốt, sẽ quay lại!"
)

print("✅ Đã tạo xong dữ liệu mẫu: ROLE, USER, SERVICE, BOOKING, PAYMENT")
