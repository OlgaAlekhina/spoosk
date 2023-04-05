# from django.shortcuts import render

from django.views.generic import ListView

from .models import SkiResort


class SkiResortList(ListView):
    model = SkiResort  # указываем модель, объекты которой мы будем выводить
    template_name = 'resorts.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'resorts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон