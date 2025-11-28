from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import (
    ClassRoom, TeacherProfile, ParentProfile, StudentProfile, Subject, Assignment,
    StudyMaterial, Notice, Event, GalleryItem, LibraryItem, Newsletter, BlogPost,
    TransportRoute, HostelRoom
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds basic demo data for the school website'

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username='admin', defaults={'role': 'admin', 'email': 'admin@example.com'})
        admin.set_password('admin123')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        parent_user, _ = User.objects.get_or_create(username='parent1', defaults={'role': 'parent', 'email': 'parent@example.com'})
        parent_user.set_password('parent123')
        parent_user.save()
        parent = ParentProfile.objects.get_or_create(user=parent_user)[0]

        teacher_user, _ = User.objects.get_or_create(username='teacher1', defaults={'role': 'teacher', 'email': 'teacher@example.com'})
        teacher_user.set_password('teacher123')
        teacher_user.save()
        teacher = TeacherProfile.objects.get_or_create(user=teacher_user, defaults={'department': 'Science'})[0]

        classroom, _ = ClassRoom.objects.get_or_create(name='Grade 10 A', grade_level='10')
        student_user, _ = User.objects.get_or_create(username='student1', defaults={'role': 'student', 'email': 'student@example.com'})
        student_user.set_password('student123')
        student_user.save()
        student = StudentProfile.objects.get_or_create(user=student_user, parent=parent, classroom=classroom)[0]

        subject, _ = Subject.objects.get_or_create(name='Mathematics', classroom=classroom, teacher=teacher)
        Assignment.objects.get_or_create(title='Algebra Homework', description='Practice problems 1-10', due_date=timezone.now().date(), classroom=classroom, subject=subject)
        StudyMaterial.objects.get_or_create(title='Algebra Notes', description='PDF notes for Algebra', subject=subject)

        Notice.objects.get_or_create(title='PTM Scheduled', body='Parent Teacher meeting on Friday', audience='parents')
        Event.objects.get_or_create(name='Science Fair', description='Annual science exhibition', date=timezone.now().date(), location='Auditorium')
        GalleryItem.objects.get_or_create(title='Campus View')
        LibraryItem.objects.get_or_create(title='To Kill a Mockingbird', author='Harper Lee')
        Newsletter.objects.get_or_create(title='Monthly Update', body='Highlights of the month')
        BlogPost.objects.get_or_create(title='Principal Message', body='Welcome to the new academic year!', author=admin)
        TransportRoute.objects.get_or_create(name='Route 1', driver='John Doe', contact='1234567890', stops='Central Park, Downtown, Riverside')
        HostelRoom.objects.get_or_create(name='Blue Dorm', capacity=20, warden_contact='warden@example.com')

        self.stdout.write(self.style.SUCCESS('Demo data seeded.'))
