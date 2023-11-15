from celery import shared_task
from django.core.mail import send_mail
from .models import InMemberShip, Member

@shared_task
def send_low_sets_remaining_email(member_email):
    subject = 'Low Sets Remaining Notification'
    message = 'Your remaining is less than 2. Please renew your membership.'
    from_email = 'your@example.com'
    recipient_list = [member_email]

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def check_and_send_emails():
    users_low_sets = InMemberShip.objects.filter(sets_remaining__lt=2).values_list('member__email', flat=True)

    for member_email in users_low_sets:
        send_low_sets_remaining_email.delay(member_email)
