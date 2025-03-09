# admin.py
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, Patient, Doctor, RoleCounter,
    PatientProxy, DoctorProxy, NurseProxy,
    LabTechProxy, RadiographerProxy, AdminProxy
)

# Inlines for related details (if you want to show details on change view)
class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'Patient Details'

class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Doctor Details'

# A generic custom creation form used only if needed (not directly used by proxy admins)
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLES)
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES, required=False)
    address = forms.CharField(required=False)
    speciality = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('role', 'name', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove role field so that it is not visible in the form.
        if 'role' in self.fields:
            del self.fields['role']

    def clean(self):
        cleaned_data = super().clean()
        # Use initial data or cleaned_data for role
        role = self.initial.get('role') or self.cleaned_data.get('role')
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
        # Save user without committing to allow modifications
        user = super().save(commit=False)
        user.save()  # Save to generate custom_id
        role = self.initial.get('role') or self.cleaned_data.get('role')
        if role == 'patient':
            Patient.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                gender=self.cleaned_data['gender'],
                address=self.cleaned_data['address']
            )
        elif role == 'doctor':
            Doctor.objects.create(user=user, speciality=self.cleaned_data['speciality'])
        if commit:
            self.save_m2m()
        return user

# Base admin class for our custom User; note that we are not exposing add permissions here.
class UserAdmin(BaseUserAdmin):
    ordering = ('custom_id',)
    add_form = CustomUserCreationForm
    list_display = ('custom_id', 'name', 'phone', 'role', 'get_specialty', 'get_age')
    readonly_fields = ('custom_id',)
    fieldsets = (
        (None, {'fields': ('role', 'phone', 'password')}),
        ('Info', {'fields': ('name', 'custom_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    # Global add_fieldsets (if needed) include all fields; however, we disable add from this view.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'password1', 'password2', 'age', 'gender', 'address', 'speciality'),
        }),
    )
    list_filter = ('role',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If used by proxy models, filter by role.
        if self.model._meta.proxy and hasattr(self.model, 'role'):
            return qs.filter(role=self.model.role)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['role', 'custom_id'] + list(super().get_readonly_fields(request, obj))
        return super().get_readonly_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Ensure role is not displayed even if present in fields.
        form.base_fields.pop('role', None)
        return form

    def save_form(self, request, form, change):
        return form.save(commit=True)

    class Media:
        js = ('admin/js/user_role.js',)

    def get_specialty(self, obj):
        return obj.doctor.speciality if hasattr(obj, 'doctor') else '-'
    get_specialty.short_description = 'Specialty'

    def get_age(self, obj):
        return obj.patient.age if hasattr(obj, 'patient') else '-'
    get_age.short_description = 'Age'

    def save_model(self, request, obj, form, change):
        # For new users coming from any add form (if reached), default to 'patient'
        if not change and not obj.role:
            obj.role = 'patient'
        super().save_model(request, obj, form, change)

# --- Role-specific creation forms ---
class DoctorCreationForm(UserCreationForm):
    speciality = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'phone', 'password1', 'password2', 'speciality')

class PatientCreationForm(UserCreationForm):
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES, required=True)
    address = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'phone', 'password1', 'password2', 'age', 'gender', 'address')

class BasicUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'phone', 'password1', 'password2')

# --- Proxy Admins for each role ---
@admin.register(AdminProxy)
class AdminAdmin(UserAdmin):
    add_form = BasicUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='admin')

    def save_model(self, request, obj, form, change):
        # Force the role to be 'admin'
        obj.role = 'admin'
        super().save_model(request, obj, form, change)

@admin.register(NurseProxy)
class NurseAdmin(UserAdmin):
    add_form = BasicUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'password1', 'password2'),
        }),
    )
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='nurse')
    
    def save_model(self, request, obj, form, change):
        # Force role to nurse
        print('Saving nurse...')
        obj.role = 'nurse'
        super().save_model(request, obj, form, change)

@admin.register(LabTechProxy)
class LabTechAdmin(UserAdmin):
    add_form = BasicUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'password1', 'password2'),
        }),
    )
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='labt')
    def save_model(self, request, obj, form, change):
        # Force role to lab tech
        obj.role = 'labt'
        super().save_model(request, obj, form, change)

@admin.register(RadiographerProxy)
class RadiographerAdmin(UserAdmin):
    add_form = BasicUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'password1', 'password2'),
        }),
    )
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='rg')
    
    def save_model(self, request, obj, form, change):
        # Force role to radiographer
        obj.role = 'rg'
        super().save_model(request, obj, form, change)

@admin.register(DoctorProxy)
class DoctorAdmin(UserAdmin):
    add_form = DoctorCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'password1', 'password2', 'speciality'),
        }),
    )
    def save_model(self, request, obj, form, change):
        # Force role to doctor
        obj.role = 'doctor'
        super().save_model(request, obj, form, change)
        if not change:
            Doctor.objects.get_or_create(
                user=obj,
                defaults={'speciality': form.cleaned_data.get('speciality', 'General Medicine')}
            )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields.pop('role', None)
        return form

@admin.register(PatientProxy)
class PatientAdmin(UserAdmin):
    add_form = PatientCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'password1', 'password2', 'age', 'gender', 'address'),
        }),
    )
    def save_model(self, request, obj, form, change):
        obj.role = 'patient'
        super().save_model(request, obj, form, change)
        if not change:
            Patient.objects.get_or_create(
                user=obj,
                defaults={
                    'age': form.cleaned_data.get('age', 0),
                    'gender': form.cleaned_data.get('gender', 'O'),
                    'address': form.cleaned_data.get('address', '')
                }
            )


# --- Global User view (read-only add) ---
@admin.register(User)
class GlobalUserAdmin(UserAdmin):
    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request)
    def has_add_permission(self, request):
        # Disable the add button from the global view so that new users
        # must be added via the role-specific proxy admin.
        return False

# Customize admin titles
admin.site.site_header = "MyHealthCard Administration"
admin.site.site_title = "User Management"
admin.site.index_title = "User Types"
