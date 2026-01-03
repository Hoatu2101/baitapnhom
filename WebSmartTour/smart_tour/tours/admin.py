from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.db.models import Sum, Count, Avg
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from . import models
from .models import User, Role, Service, Booking, BookingTour, BookingHotel, BookingTransport, Invoice, Review


# --- Role ---
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# --- User ---
class UserAdmin(DjangoUserAdmin):
    model = User

    # 1. Hiển thị ở danh sách bên ngoài
    list_display = ('username', 'email', 'role', 'is_verified', 'is_staff', 'is_active')

    # 2. Các bộ lọc nhanh bên phải
    list_filter = ('role', 'is_verified', 'is_staff', 'is_active')

    # 3. Ô tìm kiếm
    search_fields = ('username', 'email')

    # 4. THIẾT KẾ LẠI FORM CHI TIẾT (Giống ảnh bạn gửi)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),

        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'avatar')
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),

        ('Verify & Role', {
            'fields': ('role', 'is_verified'),
        }),

        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # 5. Giúp chọn nhóm quyền (Groups) dễ dàng hơn bằng 2 cột (như trong ảnh)
    filter_horizontal = ('groups', 'user_permissions')

class ServiceAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Service
        fields = '__all__'

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_date')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

# --- Service ---
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    inlines = [ReviewInline]

    list_display = (
        'id', 'name', 'service_type',
        'price', 'available_slots',
        'provider', 'avg_rating', 'review_count'
    )

    list_filter = ('service_type', 'active')
    search_fields = ('name', 'provider__username')

    def avg_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 'Chưa có'

    def review_count(self, obj):
        return obj.reviews.count()

    avg_rating.short_description = "Đánh giá TB"
    review_count.short_description = "Số đánh giá"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role and request.user.role.name == 'PROVIDER':
            return qs.filter(provider=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            if not request.user.is_verified:
                raise PermissionError("Nhà cung cấp chưa được duyệt")
            obj.provider = request.user
        super().save_model(request, obj, form, change)

    def total_revenue(self, obj):
        return f"${obj.total_revenue or 0:,.2f}"

    total_revenue.admin_order_field = 'total_revenue'
    total_revenue.short_description = 'Doanh thu'

    def total_bookings(self, obj):
        return obj.total_bookings

    total_bookings.admin_order_field = 'total_bookings'
    total_bookings.short_description = 'Số lượng đặt'
    change_list_template = "admin/tours/services/change_list.html"

    def changelist_view(self, request, extra_context=None):
        qs = self.get_queryset(request)

        chart_labels = []
        chart_booking_counts = []
        chart_revenues = []

        for service in qs:
            booking_count = service.booking_set.count()
            total_revenue = booking_count * float(service.price)

            chart_labels.append(service.name)
            chart_booking_counts.append(booking_count)
            chart_revenues.append(total_revenue)

        extra_context = extra_context or {}
        extra_context['chart_labels'] = chart_labels
        extra_context['chart_booking_counts'] = chart_booking_counts
        extra_context['chart_revenues'] = chart_revenues

        return super().changelist_view(request, extra_context=extra_context)


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

    def short_description(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "-"

    short_description.short_description = "Mô tả"

# --- Invoice ---
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_code', 'booking', 'payment_date', 'total_amount')
    list_filter = ('payment_date',)
    search_fields = ('invoice_code', 'booking__user__username')

class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'service', 'user',
        'rating', 'short_comment',
        'created_date'
    )

    list_filter = ('rating', 'created_date')
    search_fields = ('service__name', 'user__username')
    readonly_fields = ('user', 'service', 'rating', 'comment')

    def short_comment(self, obj):
        return obj.comment[:50]

    short_comment.short_description = "Nhận xét"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role and request.user.role.name == 'PROVIDER':
            return qs.filter(service__provider=request.user)
        return qs


# --- Tạo AdminSite riêng với tiêu đề + CSS ---
class MyAdminSite(admin.AdminSite):
    site_header = "XIN CHÀO !"
    site_title = "Smart Tour Admin"
    index_title = "Trang quản trị Smart Tour"

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }

    def login(self, request, extra_context=None):
            # Override login để thêm context hoặc xử lý nếu cần
            return super().login(request, extra_context=extra_context)
    def each_context(self, request):
        context = super().each_context(request)

        # Kiểm tra role
        if hasattr(request.user, 'role') and request.user.role:
            if request.user.role.name == 'Nhà cung cấp':
                context['index_title'] = "Chào mừng - nhà cung cấp"
            else:
                context['index_title'] = "Trang quản trị Smart Tour"
        return context


# --- Khởi tạo site ---
admin_site = MyAdminSite(name='myadmin')

# --- Đăng ký model vào admin_site ---
admin_site.register(User, UserAdmin)
admin_site.register(Role, RoleAdmin)
admin_site.register(Service, ServiceAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Invoice, InvoiceAdmin)
admin_site.register(Review, ReviewAdmin)

