from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role

#UserCreationForm - khung cài sẵn đăng ký thành viên của django, mã hóa dữ liệu sẵn
class SupplierRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email doanh nghiệp")



    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'avatar')

    def save(self, commit=True):
        user = super().save(commit=False)


        try:
            supplier_role = Role.objects.get(name='Nhà cung cấp')
            user.role = supplier_role
        except Role.DoesNotExist:
             print("Role chưa được tạo hoặc không phù hơp")

        user.is_verified = False

        if commit:
            user.save()
        return user