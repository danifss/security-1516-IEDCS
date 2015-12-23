from django import forms
from django.forms import ModelForm
from .models import User


class registerUserForm(ModelForm):
    # password = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="Enter password")
    # username = forms.CharField(label="Username", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}),)
    # password = forms.CharField(widget=forms.PasswordInput, required=True,)
    # email = forms.EmailField(label="Email", max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}),)
    # first_name = forms.CharField(label="First Name", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}),)
    # last_name = forms.CharField(label="Last Name", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),)

    class Meta:
        model = User
        fields = ['username', 'password', 'userCC', 'email', 'firstName', 'lastName']
        widgets = { 'password' : forms.PasswordInput() }


class loginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}),)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    # class Meta:
    #     model = User
    #     fields = ['username', 'password']
    #     widgets = { 'password' : forms.PasswordInput() }

# class AuthenticationForm(ModelForm):
#     """
#     Base class for authenticating users. Extend this to get a form that accepts
#     username/password logins.
#     """
#     # username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
#     # password = forms.CharField(label="Password", widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         widgets = { 'password' : forms.PasswordInput() }

    # error_messages = {
    #     'invalid_login': "Please enter a correct %(username)s and password. "
    #                        "Note that both fields may be case-sensitive.",
    #     'inactive': "This account is inactive.",
    # }
    #
    # def __init__(self, request=None, *args, **kwargs):
    #     """
    #     The 'request' parameter is set for custom auth use by subclasses.
    #     The form data comes in via the standard 'data' kwarg.
    #     """
    #     self.request = request
    #     self.user_cache = None
    #     super(AuthenticationForm, self).__init__(*args, **kwargs)
    #
    #     # Set the label for the "username" field.
    #     # UserModel = User
    #     # self.username_field = UserModel._meta.get_field(UserModel.username)
    #     # if self.fields['username'].label is None:
    #     #     self.fields['username'].label = capfirst(self.username_field.verbose_name)
    #     # self.fields['username'].label = 'Username'
    #
    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #
    #     if username and password:
    #         self.user_cache = authenticate(username=username,
    #                                        password=password)
    #         if self.user_cache is None:
    #             raise forms.ValidationError(
    #                 self.error_messages['invalid_login'],
    #                 code='invalid_login',
    #                 params={'username': self.username_field.verbose_name},
    #             )
    #         else:
    #             self.confirm_login_allowed(self.user_cache)
    #
    #     return self.cleaned_data
    #
    # def confirm_login_allowed(self, user):
    #     """
    #     Controls whether the given User may log in. This is a policy setting,
    #     independent of end-user authentication. This default behavior is to
    #     allow login by active users, and reject login by inactive users.
    #
    #     If the given user cannot log in, this method should raise a
    #     ``forms.ValidationError``.
    #
    #     If the given user may log in, this method should return None.
    #     """
    #     if not user.is_active:
    #         raise forms.ValidationError(
    #             self.error_messages['inactive'],
    #             code='inactive',
    #         )
    #
    # def get_user_id(self):
    #     if self.user_cache:
    #         return self.user_cache.id
    #     return None
    #
    # def get_user(self):
    #     return self.user_cache