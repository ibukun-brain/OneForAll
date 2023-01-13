from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from home.models import CustomUser
from ofa.utils.forms import CssForm

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UpdateProfileForm(UserChangeForm, CssForm):

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'additional_name',
            'username',
            'overview',
            'mobile_no',
            # 'country',
            'email',
            'overview',
            'allowed'
        ]

        labels = {
            "allowed":"Allow anyone to add you to their team",
        }

        widgets = {
            # 'mobile_no': PhoneNumberPrefixWidget(),
            'overview':forms.Textarea(
                attrs={
                    "rows":4
                }
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email address", "readonly": True}
            ),
            'allowed':forms.CheckboxInput(
                    attrs={
                        "class":"form-check-input",
                    }
                )
        }

class UpdateProfilePicForm(UserChangeForm, CssForm):

    class Meta:
        model = CustomUser
        fields = ['profile_pic']

class ChangePasswordForm(PasswordChangeForm, CssForm):
    
    class Meta:
        model = CustomUser
        fields = '__all__'

        labels = {
            "old_password":"Old Password",
            "new_password1":"New Password",
            "new_password2":"New Password Confirmation"
        }

