from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Account


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'nickname')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password Don't Match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('username', 'nickname', 'address', 'email', 'is_admin')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'nickname', 'address',
                    'email', 'is_admin', 'avatar')
    list_filter = ('is_admin', 'username')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'address', 'password')}),
        ('Personal info', {'fields': ('nickname', 'avatar')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fields = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nickname', 'avatar', 'password1', 'password2', 'email', 'address')}
         ),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(Account, UserAdmin)
admin.site.unregister(Group)
