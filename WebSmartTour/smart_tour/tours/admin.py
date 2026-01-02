from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.db.models import Sum, Count
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Role, Service, Booking, BookingTour, BookingHotel, BookingTransport, Invoice


# --- Role ---
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# --- User ---
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    

class ServiceAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Service
        fields = '__all__'


# --- Service ---
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm

    list_display = (
        'id', 'name', 'service_type',
        'price', 'available_slots',
        'provider', 'total_revenue', 'total_bookings'
    )

    list_filter = ('service_type', 'active')
    search_fields = ('name', 'provider__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            total_revenue=Sum('booking__invoice__total_amount'),
            total_bookings=Count('booking')
        )
        return qs

    def total_revenue(self, obj):
        return f"${obj.total_revenue or 0:,.2f}"

    total_revenue.admin_order_field = 'total_revenue'
    total_revenue.short_description = 'Doanh thu'

    def total_bookings(self, obj):
        return obj.total_bookings

    total_bookings.admin_order_field = 'total_bookings'
    total_bookings.short_description = 'Số lượng đặt'

    #Chỉ nhà cung cấp mới được tạo dịch vụ
    def save_model(self, request, obj, form, change):
        if not change:
            obj.provider = request.user
        super().save_model(request, obj, form, change)


# --- Inline cho Booking ---
class BookingTourInline(admin.StackedInline):
    model = BookingTour
    extra = 0


class BookingHotelInline(admin.StackedInline):
    model = BookingHotel
    extra = 0


class BookingTransportInline(admin.StackedInline):
    model = BookingTransport
    extra = 0


# --- Booking ---
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'booking_date', 'active', 'created_date')
    list_filter = ('service', 'active', 'booking_date')
    search_fields = ('user__username', 'service__name')
    inlines = [BookingTourInline, BookingHotelInline, BookingTransportInline]


# --- Invoice ---
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_code', 'booking', 'payment_date', 'total_amount')
    list_filter = ('payment_date',)
    search_fields = ('invoice_code', 'booking__user__username')


# --- Tạo AdminSite riêng với tiêu đề + CSS ---
class MyAdminSite(admin.AdminSite):
    site_header = "Chào mừng tới trang quản trị"
    site_title = "Smart Tour Admin"
    index_title = "Trang quản trị Smart Tour"

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }


# --- Khởi tạo site ---
admin_site = MyAdminSite(name='myadmin')

# --- Đăng ký model vào admin_site ---
admin_site.register(User, UserAdmin)
admin_site.register(Role, RoleAdmin)
admin_site.register(Service, ServiceAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Invoice, InvoiceAdmin)
