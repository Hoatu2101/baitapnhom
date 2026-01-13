from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role

class SupplierRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Họ")
    last_name = forms.CharField(required=True, label="Tên")
    email = forms.EmailField(required=True, label="Email doanh nghiệp")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        # Gán role PROVIDER
        try:
            supplier_role = Role.objects.get(name='PROVIDER')
            user.role = supplier_role
        except Role.DoesNotExist:
            print("Role PROVIDER chưa tồn tại")

        user.is_verified = False

        if commit:
            user.save()
        return user
