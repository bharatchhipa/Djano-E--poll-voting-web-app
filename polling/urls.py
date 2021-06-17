from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginhandle, name='login'),
    path('logout', views.logouthandle, name='logout'),
    path('contact', views.contact, name='contact'),
    path('register', views.register, name='register'),
    path('results', views.results, name='result'),
    path('logout',views.logouthandle, name='logout'),
    path('votingpanel',views.votingpanel,name='voting'),
    path('candidate',views.candidate,name='candidate'),
    path('verify',views.aadharverify,name='verify'),
    path('OTP',views.otp,name='OTP'),
    path('vote<sno>',views.vote,name='vote'),
    path('adminpanel',views.show_results,name='admin')

]