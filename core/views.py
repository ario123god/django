from datetime import date
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import StudentRegistrationForm, ParentRegistrationForm, AdmissionForm, ContactForm
from .models import (
    Assignment, AttendanceRecord, BlogPost, ClassRoom, Event, GalleryItem, Grade,
    LibraryItem, Newsletter, Notice, ReportCard, StudyMaterial, Subject, TimetableEntry,
    AdmissionApplication, FeePayment, TransportRoute, HostelRoom
)


def home(request):
    stats = {
        'students': 1200,
        'teachers': 85,
        'programs': 42,
        'alumni': 5200,
    }
    events = Event.objects.all()[:3]
    notices = Notice.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', {'stats': stats, 'events': events, 'notices': notices})


def about(request):
    return render(request, 'about.html')


def programs(request):
    subjects = Subject.objects.select_related('teacher', 'classroom')
    labs = ['Physics Lab', 'Chemistry Lab', 'Computer Lab']
    timetable = TimetableEntry.objects.select_related('subject', 'classroom')[:10]
    return render(request, 'programs.html', {'subjects': subjects, 'labs': labs, 'timetable': timetable})


def admissions(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('admissions')
    else:
        form = AdmissionForm()
    downloads = [
        {'title': 'School Prospectus', 'url': '#'},
        {'title': 'Fee Structure', 'url': '#'},
    ]
    applications = AdmissionApplication.objects.order_by('-submitted_on')[:5]
    return render(request, 'admissions.html', {'form': form, 'downloads': downloads, 'applications': applications})


def fees(request):
    scholarships = [
        {'name': 'Merit Scholarship', 'detail': 'For top-performing students'},
        {'name': 'Need-Based Aid', 'detail': 'Assistance for eligible families'},
    ]
    return render(request, 'fees.html', {'scholarships': scholarships})


def events(request):
    gallery = GalleryItem.objects.order_by('-created_at')
    event_list = Event.objects.order_by('date')
    return render(request, 'events.html', {'gallery': gallery, 'events': event_list})


def faculty(request):
    teachers = ClassRoom.objects.prefetch_related('subjects__teacher')
    return render(request, 'faculty.html', {'teachers': teachers})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent! We will respond soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def faq_notices(request):
    faqs = [
        {'question': 'What is the admission process?', 'answer': 'Submit the online form and await approval.'},
        {'question': 'Do you offer transport?', 'answer': 'Yes, safe and GPS-enabled buses across the city.'},
    ]
    notices = Notice.objects.order_by('-created_at')
    return render(request, 'faq.html', {'faqs': faqs, 'notices': notices})


def library(request):
    items = LibraryItem.objects.all()
    return render(request, 'library.html', {'items': items})


def news(request):
    posts = BlogPost.objects.order_by('-published_on')
    newsletters = Newsletter.objects.order_by('-published_on')
    return render(request, 'news.html', {'posts': posts, 'newsletters': newsletters})


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.save()
            login(request, user)
            messages.success(request, 'Welcome to the student portal!')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form, 'title': 'Student Registration'})


def register_parent(request):
    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'parent'
            user.save()
            login(request, user)
            messages.success(request, 'Parent account created!')
            return redirect('dashboard')
    else:
        form = ParentRegistrationForm()
    return render(request, 'register.html', {'form': form, 'title': 'Parent Registration'})


class RoleLoginView(LoginView):
    template_name = 'login.html'


class RoleLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class RolePasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'emails/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class RolePasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class RolePasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class RolePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


@login_required
def dashboard(request):
    user = request.user
    context = {'today': date.today()}
    if user.role == 'student':
        context.update({
            'assignments': Assignment.objects.all()[:5],
            'materials': StudyMaterial.objects.all()[:5],
            'attendance': AttendanceRecord.objects.filter(student__user=user)[:5],
            'grades': Grade.objects.filter(student__user=user)[:5],
            'timetable': TimetableEntry.objects.select_related('subject')[:6],
        })
    elif user.role == 'parent':
        context.update({
            'fees': FeePayment.objects.all()[:5],
            'notices': Notice.objects.filter(audience__in=['parents', 'all'])[:5],
        })
    elif user.role == 'teacher':
        context.update({
            'classes': ClassRoom.objects.all(),
            'assignments': Assignment.objects.all()[:5],
        })
    else:
        context.update({
            'applications': AdmissionApplication.objects.order_by('-submitted_on')[:5],
            'analytics': {
                'students': Assignment.objects.count(),
                'attendance': AttendanceRecord.objects.count(),
                'events': Event.objects.count(),
            },
        })
    return render(request, 'dashboard.html', context)


def transport_hostel(request):
    routes = TransportRoute.objects.all()
    hostels = HostelRoom.objects.all()
    return render(request, 'transport_hostel.html', {'routes': routes, 'hostels': hostels})
