from django.shortcuts import render
from .forms import RegisterForm
from django.views import generic
from django.urls import reverse_lazy


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


