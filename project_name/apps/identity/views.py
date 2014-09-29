"""
Identity views
"""
import re

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from .forms import UserCreationForm, LoginForm, UserEditForm
from .models import Identity


class Register(generic.edit.CreateView):
    """
    Register a new user.
    """
    form_class = UserCreationForm
    template_name = 'identity/register.html'

    def get_success_url(self):
        """
        Redirect after a successful registration
        """
        return reverse('homepage')

    def form_valid(self, form):
        """
        Log the user in on a successful request.
        """
        response = super(Register, self).form_valid(form)

        username = form.cleaned_data['email']
        password = form.cleaned_data['password1']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                from django.contrib.auth import login
                login(self.request, user)

        return response


class Edit(generic.edit.UpdateView):
    """
    User profile editing
    """
    template_name = 'identity/edit.html'
    form_class = UserEditForm
    success_url = reverse_lazy('homepage')
    model = Identity

    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Edit, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.password_form = SetPasswordForm(user=request.user)
        return super(Edit, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        forms_valid = True
        change_password = False

        form = self.get_form(self.get_form_class())
        if not form.is_valid():
            forms_valid = False

        if self.request.POST.get('new_password1'):
            change_password = True
            self.password_form = SetPasswordForm(
                data=request.POST, user=request.user)

            if not self.password_form.is_valid():
                forms_valid = False
        else:
            self.password_form = SetPasswordForm(user=request.user)

        if forms_valid:
            form.save()
            if change_password:
                self.password_form.save()

            self.notifications_form.save()

            return HttpResponseRedirect(self.get_success_url())

        else:
            return self.render_to_response(
                self.get_context_data(form=form))

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        return super(Edit, self).get_context_data(
            password_form=self.password_form,
            notifications_form=self.notifications_form,
            **kwargs
        )

