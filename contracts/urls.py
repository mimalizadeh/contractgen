from django.urls import path
from . import views

urlpatterns = [
    path('template/', view=views.pdf_template, name="pdf_template")

]
