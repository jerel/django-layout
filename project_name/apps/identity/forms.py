
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import Identity


class UserChangeForm(forms.ModelForm):
    """
    Used by the django admin
    """
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = Identity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email address"))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                try:
                    # get the user account so we can test if they are banned
                    user_account = Identity.objects.get(email=email)
                except:
                    user_account = None

                # password is set to "unusable" and they are inactive
                if user_account and user_account.is_active is False:
                    raise forms.ValidationError(
                        _("This account is inactive."))
                # the account is active so they must have the wrong credentials
                else:
                    raise forms.ValidationError(
                        _("Incorrect email address or password."))
            elif not user.is_active:
                raise forms.ValidationError(_("This account is inactive."))
            self.cleaned_data['user'] = user

        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't "
                    "appear to have cookies enabled. Cookies are required "
                    "for logging in."))

        return self.cleaned_data


class UserCreationForm(forms.ModelForm):
    """

    """

    error_messages = {
        'duplicate_user': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        fields = ('first_name', 'last_name', 'email')
        model = Identity

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Identity.objects.get(email=email)
        except Identity.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_user'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    """
    Edit user model form
    """
    class Meta:
        model = Identity
        fields = ('first_name', 'last_name', 'email', )

