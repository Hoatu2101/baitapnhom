from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView
from smart_tour import settings
from . import views
from .views import UserView

router = DefaultRouter()
router.register('services', views.ServiceView, basename='service')
router.register('bookings', views.BookingView, basename='booking')
router.register('reviews', views.ReviewView, basename='review')
router.register('payments', views.PaymentView, basename='payment')
router.register("users", views.UserView, basename="user")


urlpatterns = [
    path('api/', include(router.urls)),
    path("api/users/", UserView.as_view({"post": "create"})),

    path("api/register/", RegisterView.as_view()),

    path('reports/provider/', views.ProviderReportView.as_view()),
    path('reports/admin/', views.AdminReportView.as_view()),

    path('register_supplier/', views.register_supplier, name='register_supplier'),
    path('', views.intro_supplier, name='intro_supplier'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)