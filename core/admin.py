from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User, ParentProfile, TeacherProfile, StudentProfile, ClassRoom, Subject,
    SyllabusItem, TimetableEntry, Assignment, StudyMaterial, Notice, Event,
    GalleryItem, AttendanceRecord, Grade, FeePayment, ReportCard, TransportRoute,
    HostelRoom, LibraryItem, HomeworkSubmission, Newsletter, BlogPost,
    ContactMessage, AdmissionApplication, OTPVerification
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role', {'fields': ('role', 'phone', 'verified')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'verified')
    list_filter = ('role', 'verified')


admin.site.register([
    ParentProfile, TeacherProfile, StudentProfile, ClassRoom, Subject, SyllabusItem,
    TimetableEntry, Assignment, StudyMaterial, Notice, Event, GalleryItem,
    AttendanceRecord, Grade, FeePayment, ReportCard, TransportRoute, HostelRoom,
    LibraryItem, HomeworkSubmission, Newsletter, BlogPost, ContactMessage,
    AdmissionApplication, OTPVerification
])
