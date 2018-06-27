from django.contrib import admin

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from audit import models
# Register your models here.

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email','name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password not match")
        return password2

    def save(self,commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = models.UserProfile
        fields = ('email','password','name','is_active','is_superuser')

    def clean_password(self):
        return self.initial["password"]

class UserProfileAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email','name','is_active','is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None,{'fields':('email','password')}),
        ('Personal',{'fields':('name',)}),
        ('Permissions',{'fields':('is_superuser','is_active','bind_hosts','host_groups','user_permissions','groups')}),

    )

    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','name','password1','password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ("bind_hosts","host_groups","user_permissions","groups")




class HostUserAdmin(admin.ModelAdmin):
    list_display = ('username','auth_type','password')

admin.site.register(models.UserProfile,UserProfileAdmin)
admin.site.register(models.Host)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUser,HostUserAdmin)
admin.site.register(models.BindHost)
admin.site.register(models.IDC)
