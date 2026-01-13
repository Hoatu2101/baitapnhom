# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views
#
# router = DefaultRouter()
# router.register('roles', views.RoleView, basename='role')
# router.register('users', views.UserView, basename='user')
# router.register('services', views.ServiceView, basename='service')
# router.register('bookings', views.BookingView, basename='booking')
# router.register('booking-tours', views.BookingTourView, basename='booking-tour')
# router.register('booking-hotels', views.BookingHotelView, basename='booking-hotel')
# router.register('booking-transports', views.BookingTransportView, basename='booking-transport')
# router.register('payments', views.PaymentView, basename='payment')
# router.register('reviews', views.ReviewView, basename='review')
#
# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('reports/provider/', views.ProviderReportView.as_view()),
#     path('reports/admin/', views.AdminReportView.as_view()),
#     path('register_supplier/', views.register_supplier, name='register_supplier'),
#     path('', views.intro_supplier, name='intro_supplier'),
# ]
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from smart_tour import settings
from . import views

router = DefaultRouter()
router.register('services', views.ServiceView, basename='service')
router.register('bookings', views.BookingView, basename='booking')
router.register('reviews', views.ReviewView, basename='review')
router.register('payments', views.PaymentView, basename='payment')
router.register("users", views.UserView, basename="user")


urlpatterns = [
    path('api/', include(router.urls)),

    path('reports/provider/', views.ProviderReportView.as_view()),
    path('reports/admin/', views.AdminReportView.as_view()),
    path('login/', views.login_supplier, name='login'),
    path('register_supplier/', views.register_supplier, name='register_supplier'),
    path('', views.intro_supplier, name='intro_supplier'),
    path('accounts/', include('django.contrib.auth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)