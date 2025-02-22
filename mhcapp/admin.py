# Register your models here.
from django.contrib import admin
from django import forms

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, Doctor, RoleCounter
from django.contrib.auth.forms import UserCreationForm

class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'Patient Details'

class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Doctor Details'

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLES)
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES, required=False)
    address = forms.CharField(required=False)
    speciality = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('role', 'name', 'phone', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role == 'patient':
            if not cleaned_data.get('age'):
                self.add_error('age', 'Required for patients.')
            if not cleaned_data.get('gender'):
                self.add_error('gender', 'Required for patients.')
            if not cleaned_data.get('address'):
                self.add_error('address', 'Required for patients.')
        elif role == 'doctor' and not cleaned_data.get('speciality'):
            self.add_error('speciality', 'Required for doctors.')
        return cleaned_data

    def save(self, commit=True):
        # Save the user first without committing
        user = super().save(commit=False)
        # Manually save to generate ID/custom_id
        user.save()

        # Create related models
        role = self.cleaned_data.get('role')
        if role == 'patient':
            Patient.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                gender=self.cleaned_data['gender'],
                address=self.cleaned_data['address']
            )
        elif role == 'doctor':
            Doctor.objects.create(user=user, speciality=self.cleaned_data['speciality'])
        
        # Save any many-to-many relationships
        if commit:
            self.save_m2m()

        return user

class UserAdmin(BaseUserAdmin):
    # To specify ordering by phone number or custom_id
    ordering = ('custom_id',)  # or ('phone',)
    add_form = CustomUserCreationForm
    list_display = ('custom_id', 'name', 'phone', 'role')
    readonly_fields = ('custom_id',)
    fieldsets = (
        (None, {'fields': ('role', 'phone', 'password')}),
        ('Info', {'fields': ('name', 'custom_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('role', 'name', 'phone', 'password1', 'password2', 'age', 'gender', 'address', 'speciality'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['role', 'custom_id'] + list(super().get_readonly_fields(request, obj))
        return super().get_readonly_fields(request, obj)

    def get_inlines(self, request, obj=None):
        if obj and obj.role == 'patient':
            return [PatientInline]
        elif obj and obj.role == 'doctor':
            return [DoctorInline]
        return []
    
    def save_form(self, request, form, change):
        # This ensures proper handling of the user instance
        return form.save(commit=True)  # Explicitly commit changes

    class Media:
        js = ('admin/js/user_role.js',)

admin.site.register(User, UserAdmin)
