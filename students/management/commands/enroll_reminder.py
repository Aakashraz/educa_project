import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone
from textwrap import dedent



class Command(BaseCommand):
    help = 'Send an e-mail reminder to users registered more than' \
            'N days that are not enrolled into any courses yet'

    def add_arguments(self, parser):
        parser.add_argument('--days', dest='days', type=int, default=7)

    def handle(self, *args, **options):
        emails = []
        subject = 'Enroll in a course'
        # date_joined is the User's date of registration field in a User model
        # But also used as a cutoff date to filter users
        date_joined = timezone.now().date() - datetime.timedelta(days=options['days'])
        users = User.objects.annotate(
            course_count=Count('courses_joined')
        ).filter(course_count=0, date_joined__date__lte=date_joined)
        # date_joined_date=date_joined --> 2026-08-10 14:35:22 → strips to → 2026-08-10 ← then compares
        for user in users:
            message = dedent(f"""\
                Dear {user.first_name},
                We noticed that you didn't enroll in any course yet.
                What are you waiting for?
                Enroll now!
            """)
            emails.append(
                (
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )
            )
        send_mass_mail(emails)
        self.stdout.write(f'Sent {len(emails)} reminders')
        # self.stdout.write is used instead of print because management commands have their
        # own output stream — it respects --verbosity flags and can be redirected properly.