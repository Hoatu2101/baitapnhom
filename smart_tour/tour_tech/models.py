from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    def __str__(self):
        return self.username
# id_service tự động là id mặc định của Django

# thông tin dịch vụ
class Service(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name


class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()

    def __str__(self):
        return f"Booking {self.id} by {self.user}"


class BookingTour(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    departure_date = models.DateField()
    return_date = models.DateField()
    transport = models.CharField(max_length=100)
    hotel_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Tour booking {self.booking.id}"


class BookingHotel(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    hotel_name = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"Hotel booking {self.booking.id}"


class BookingTransport(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    transport_type = models.CharField(max_length=100)
    departure_date = models.DateField()

    def __str__(self):
        return f"Transport booking {self.booking.id}"


class Invoice(models.Model):
    invoice_code = models.CharField(max_length=100, unique=True)  # mã HD
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.invoice_code}"
