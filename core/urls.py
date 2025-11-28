from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    home, about, programs, admissions, fees, events, faculty, contact,
    faq_notices, library, news, register_parent, register_student, RoleLoginView,
    RoleLogoutView, RolePasswordResetView, RolePasswordResetDoneView,
    RolePasswordResetConfirmView, RolePasswordResetCompleteView, dashboard,
    transport_hostel
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('programs/', programs, name='programs'),
    path('admissions/', admissions, name='admissions'),
    path('fees/', fees, name='fees'),
    path('events/', events, name='events'),
    path('faculty/', faculty, name='faculty'),
    path('contact/', contact, name='contact'),
    path('faq/', faq_notices, name='faq'),
    path('library/', library, name='library'),
    path('news/', news, name='news'),
    path('transport/', transport_hostel, name='transport'),
    path('register/student/', register_student, name='register_student'),
    path('register/parent/', register_parent, name='register_parent'),
    path('login/', RoleLoginView.as_view(), name='login'),
    path('logout/', RoleLogoutView.as_view(), name='logout'),
    path('password_reset/', RolePasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', RolePasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', RolePasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', RolePasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/', dashboard, name='dashboard'),
]
