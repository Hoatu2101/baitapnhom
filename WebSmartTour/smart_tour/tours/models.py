from ckeditor_uploader.fields import RichTextUploadingField
from cloudinary.models import CloudinaryField
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
    avatar = CloudinaryField(null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()

    is_verified = models.BooleanField(default=False)  # duyệt nhà cung cấp

    def __str__(self):
        return self.username


# thông tin dịch vụ
class Service(BaseModel):
    SERVICE_TYPES = (
        ('TOUR', 'Tour du lịch'),
        ('HOTEL', 'Khách sạn'),
        ('TRANSPORT', 'Phương tiện di chuyển'),
    )

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    image = CloudinaryField(null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateTimeField()
    available_slots = models.IntegerField(null=True, blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)

    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='services'
    )

    def __str__(self):
        return self.name

class Review(BaseModel):
    RATING_CHOICES = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    class Meta:
        unique_together = ('user', 'service')
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.service.name} - {self.rating}⭐ by {self.user.username}"



class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    description = RichTextUploadingField(null=True, blank=True)

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
