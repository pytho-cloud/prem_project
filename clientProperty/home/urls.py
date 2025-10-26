from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('save-lead/', views.save_lead, name='save_lead'),
    path('about/', views.about, name="about"),
    # path('contact/', views.contact, name="contact"),
    path('properties/',views.properties ,name = 'properties'),
    path('submit-contact/', views.submit_contact, name='submit_contact'),
    path('contact/', views.contact_view, name='contact'),
]
