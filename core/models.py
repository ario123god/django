from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin/Owner'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    verified = models.BooleanField(default=False)

    def display_role(self):
        return dict(self.ROLE_CHOICES).get(self.role, 'Member')


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    address = models.CharField(max_length=255, blank=True)
    emergency_contact = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"


class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.name} ({self.grade_level})"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    room = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    parent = models.ForeignKey(ParentProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    enrollment_date = models.DateField(default=timezone.now)
    roll_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Student: {self.user.get_full_name()}"


class Subject(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, related_name='subjects')

    def __str__(self):
        return self.name


class SyllabusItem(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='syllabus_items')
    topic = models.CharField(max_length=200)
    week = models.PositiveIntegerField(default=1)
    resources = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject.name}: {self.topic}"


class TimetableEntry(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='timetable_entries')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.classroom} - {self.subject}"


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class StudyMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    url = models.URLField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='materials')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Notice(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    audience = models.CharField(max_length=20, choices=[('all', 'All'), ('students', 'Students'), ('parents', 'Parents'), ('teachers', 'Teachers')], default='all')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    registration_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AttendanceRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], default='Present')

    def __str__(self):
        return f"{self.student} - {self.date} ({self.status})"


class Grade(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"


class FeePayment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(default=timezone.now)
    reference = models.CharField(max_length=100, blank=True)
    method = models.CharField(max_length=50, default='Manual')

    def __str__(self):
        return f"{self.student} - {self.amount}"


class ReportCard(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='report_cards')
    term = models.CharField(max_length=100)
    issued_on = models.DateField(default=timezone.now)
    pdf = models.FileField(upload_to='report_cards/', blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.term}"


class TransportRoute(models.Model):
    name = models.CharField(max_length=200)
    driver = models.CharField(max_length=120)
    contact = models.CharField(max_length=120)
    stops = models.TextField(help_text='List of stops')

    def __str__(self):
        return self.name


class HostelRoom(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=2)
    warden_contact = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class LibraryItem(models.Model):
    TYPE_CHOICES = [('book', 'Book'), ('ebook', 'eBook')]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    item_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='book')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class HomeworkSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='homework/', blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.assignment} - {self.student}"


class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    published_on = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    published_on = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


class AdmissionApplication(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    student_name = models.CharField(max_length=200)
    parent_email = models.EmailField()
    grade_applied = models.CharField(max_length=100)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application: {self.student_name}"


class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp_verification')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.username}"
