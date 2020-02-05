from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from register.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_author")

    # implement this validation as Django thinks that email is case sensitive
    def clean_email(self):
        email = self.cleaned_data["email"]

        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("A user with that email already exists."),
                code='email_exists')

        return email

    # implement this validation as Django thinks that username is case sensitive
    def clean_username(self):
        username = self.cleaned_data['username']

        # we don't allow username to be in email format as email is also a field for authentication
        try:
            validate_email(data)            
        except:
            if username and User.objects.filter(username__iexact=username).exists():
                raise ValidationError(_("A user with that username already exists."), 
                    code='user_exists')    
        else:
            raise ValidationError(_("Username can't be of Email format"), 
                    code='username_in_email_format')

        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if self.cleaned_data['is_author']:
                g = Group.objects.get(name='blog_authors')
                user.groups.add(g)
        return user