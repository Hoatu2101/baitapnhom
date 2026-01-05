from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('roles', views.RoleView, basename='role')
router.register('users', views.UserView, basename='user')
router.register('services', views.ServiceView, basename='service')
router.register('bookings', views.BookingView, basename='booking')
router.register('booking-tours', views.BookingTourView, basename='booking-tour')
router.register('booking-hotels', views.BookingHotelView, basename='booking-hotel')
router.register('booking-transports', views.BookingTransportView, basename='booking-transport')
router.register('invoices', views.InvoiceView, basename='invoice')
router.register('reviews', views.ReviewView, basename='review')


urlpatterns = [
    path('api', include(router.urls)),
    path('register_supplier/', views.register_supplier, name='register_supplier'),
    path('', views.intro_supplier, name='intro_supplier'),
]
