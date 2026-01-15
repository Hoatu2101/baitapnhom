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
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    avatar = CloudinaryField(null=True, blank=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Service(BaseModel):
    SERVICE_TYPES = (
        ('TOUR', 'Tour'),
        ('HOTEL', 'Hotel'),
        ('TRANSPORT', 'Transport'),
    )

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    image = CloudinaryField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateTimeField()
    available_slots = models.IntegerField(null=True, blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)

    provider = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='services'
    )

    def __str__(self):
        return self.name


class Booking(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    booking_date = models.DateTimeField()
    description = RichTextUploadingField(null=True, blank=True)

    def __str__(self):
        return f"Booking #{self.id}"


class BookingTour(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name='tour_detail'
    )
    departure_date = models.DateField()
    return_date = models.DateField()
    transport = models.CharField(max_length=100)
    hotel_name = models.CharField(max_length=100)


class BookingHotel(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name='hotel_detail'
    )
    hotel_name = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()


class BookingTransport(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name='transport_detail'
    )
    transport_type = models.CharField(max_length=100)
    departure_date = models.DateField()


class Review(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    class Meta:
        unique_together = ('user', 'service')
        ordering = ['-created_date']


class Payment(BaseModel):
    METHOD_CHOICES = (
        ('CASH', 'Cash'),
        ('PAYPAL', 'PayPal'),
        ('STRIPE', 'Stripe'),
        ('MOMO', 'MoMo'),
        ('ZALOPAY', 'ZaloPay'),
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.PROTECT,
        related_name='payment'
    )
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)


class Invoice(models.Model):
    invoice_code = models.CharField(max_length=100, unique=True)
    booking = models.OneToOneField(
        Booking,
        on_delete=models.PROTECT,
        related_name='invoice'
    )
    payment_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)