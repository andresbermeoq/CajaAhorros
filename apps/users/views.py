from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.views.generic import CreateView, View
from django.views.generic.edit import FormView

from .forms import userRegisterForm, loginUserForm, updatePasswordForm, verifyUserForm
from .models import User
from .functions import codeGenerator


class userRegisterView(FormView):
  template_name = 'user/register.html'
  form_class = userRegisterForm
  success_url = '/'

  def form_valid(self, form):
    # Function that generates a Random Registration Code
    codeRandom = codeGenerator()

    usuario = User.objects.create_user(
      form.cleaned_data['username'],
      form.cleaned_data['email'],
      form.cleaned_data['dateBirth'],
      form.cleaned_data['password1'],
      IDCard = form.cleaned_data['IDCard'],
      name = form.cleaned_data['name'],
      last_name = form.cleaned_data['last_name'],
      address = form.cleaned_data['address'],
      phone = form.cleaned_data['phone'],
      codeRegister = codeRandom
    )
    subject = 'Confirmacion de Email'
    message = 'Codigo de Verificacion: ' + codeRandom
    emailSender = 'andipandi467@gmail.com'
    send_mail(subject, message, emailSender, [form.cleaned_data['email'], ])

    return HttpResponseRedirect(
        reverse(
            'user_app:user-verification',
            kwargs = { 'pk' : usuario.id}
        )
      )


class loginUserView(FormView):
  template_name = 'user/login.html'
  form_class = loginUserForm
  success_url = reverse_lazy('home_app:panel')

  def form_valid(self, form):
    user = authenticate(
      username = form.cleaned_data['username'],
      password = form.cleaned_data['password']
    )

    login(self.request, user)
    return super(loginUserView, self).form_valid(form)

class logoutUserView(View):

  def get(self, request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect(reverse('user_app:login-register'))

class updatePasswordView(FormView):
  template_name = 'user/update.html'
  form_class = updatePasswordForm
  success_url = reverse_lazy('user_app:login-register')

  def form_valid(self, form):
    usuario = self.request.user
    user = authenticate(
      username = usuario.username,
      password = form.cleaned_data['passwordCurrent']
    )

    if user:
      passwordNew = form.cleaned_data['passwordNew']
      usuario.set_password(passwordNew)
      usuario.save()

    logout(self.request)
    return super(updatePasswordView, self).form_valid(form)

class codeVerificationView(FormView):
  template_name = 'user/verify.html'
  form_class = verifyUserForm
  success_url = reverse_lazy('user_app:login-register')

  def get_form_kwargs(self):
    kwargs = super(codeVerificationView, self).get_form_kwargs()
    kwargs.update(
      {
        'pk' : self.kwargs['pk'],
      }
    )
    return kwargs

  def form_valid(self, form):
    User.objects.filter(
      id = self.kwargs['pk']
    ).update(is_active = True)
    return super(codeVerificationView, self).form_valid(form)

