from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin
from django.db.models import Avg

from .models import User, Role, Service, Booking, BookingTour, BookingHotel, BookingTransport, Invoice, Review

def filter_by_provider(qs, request, lookup):
    if request.user.is_superuser:
        return qs
    if request.user.role and request.user.role.name == 'Nhà cung cấp':
        return qs.filter(**{lookup: request.user})
    return qs.none()


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('Phân quyền', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Xác thực & Vai trò', {'fields': ('role', 'is_verified')}),
        ('Ngày quan trọng', {'fields': ('last_login', 'date_joined')}),
    )
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


class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    inlines = [ReviewInline]
    list_display = ('id', 'name', 'service_type', 'price', 'available_slots', 'provider', 'avg_rating', 'review_count')
    list_filter = ('service_type', 'active')
    search_fields = ('name', 'provider__username')
    change_list_template = "admin/tours/services/change_list.html"
    def changelist_view(self, request, extra_context=None):
        qs = self.get_queryset(request)
        chart_labels = []
        chart_booking_counts = []
        chart_revenues = []
        for service in qs:
            booking_count = service.bookings.count()
            total_revenue = booking_count * float(service.price)
            chart_labels.append(service.name)
            chart_booking_counts.append(booking_count)
            chart_revenues.append(total_revenue)
        extra_context = extra_context or {}
        extra_context['chart_labels'] = chart_labels
        extra_context['chart_booking_counts'] = chart_booking_counts
        extra_context['chart_revenues'] = chart_revenues
        return super().changelist_view(request, extra_context=extra_context)
    def avg_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 'Chưa có'
    avg_rating.short_description = "Đánh giá TB"

    def review_count(self, obj):
        return obj.reviews.count()
    review_count.short_description = "Số đánh giá"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_by_provider(qs, request, 'provider')

    def save_model(self, request, obj, form, change):
        if not change:
            if not request.user.is_verified:
                raise PermissionError("Nhà cung cấp chưa được duyệt")
            obj.provider = request.user
        super().save_model(request, obj, form, change)


class BookingTourInline(admin.StackedInline):
    model = BookingTour
    extra = 0


class BookingHotelInline(admin.StackedInline):
    model = BookingHotel
    extra = 0


class BookingTransportInline(admin.StackedInline):
    model = BookingTransport
    extra = 0


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'booking_date', 'active', 'created_date')
    list_filter = ('service', 'active', 'booking_date')
    search_fields = ('user__username', 'service__name')
    inlines = [BookingTourInline, BookingHotelInline, BookingTransportInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_by_provider(qs, request, 'service__provider')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'service':
            if request.user.role and request.user.role.name == 'Nhà cung cấp':
                kwargs['queryset'] = Service.objects.filter(provider=request.user)
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_list_filter(self, request):
        if request.user.role and request.user.role.name == 'Nhà cung cấp':
            return ('active', 'booking_date',)
        return self.list_filter

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if request.user.role and request.user.role.name == 'Nhà cung cấp':
            queryset = queryset.filter(service__provider=request.user)
        return queryset, use_distinct


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_code', 'booking', 'payment_date', 'total_amount')
    list_filter = ('payment_date',)
    search_fields = ('invoice_code', 'booking__user__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_by_provider(qs, request, 'booking__service__provider')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'booking':
            if request.user.role and request.user.role.name == 'Nhà cung cấp':
                kwargs['queryset'] = Booking.objects.filter(service__provider=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_list_filter(self, request):
        if request.user.role and request.user.role.name == 'Nhà cung cấp':
            return ('payment_date',)
        return self.list_filter

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if request.user.role and request.user.role.name == 'Nhà cung cấp':
            queryset = queryset.filter(booking__service__provider=request.user)
        return queryset, use_distinct


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'rating', 'short_comment', 'created_date')
    list_filter = ('rating', 'created_date')
    search_fields = ('service__name', 'user__username')
    readonly_fields = ('user', 'service', 'rating', 'comment')

    def short_comment(self, obj):
        return obj.comment[:50]
    short_comment.short_description = "Nhận xét"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_by_provider(qs, request, 'service__provider')


class MyAdminSite(admin.AdminSite):
    site_header = "XIN CHÀO !"
    site_title = "Smart Tour Admin"
    index_title = "Trang quản trị Smart Tour"

    class Media:
        css = {'all': ('css/custom_admin.css',)}


admin_site = MyAdminSite(name='myadmin')
admin_site.register(User, UserAdmin)
admin_site.register(Role, RoleAdmin)
admin_site.register(Service, ServiceAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Invoice, InvoiceAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(Group, GroupAdmin)