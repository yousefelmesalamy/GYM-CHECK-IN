from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.conf import settings
from datetime import datetime
from datetime import date, timedelta
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

DAYS_OF_WEEK_CHOICES = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('SATURDAY, SUNDAY, MONDAY', 'SATURDAY, SUNDAY, MONDAY'),
    ('SUNDAY, MONDAY, TUESDAY', 'SUNDAY, MONDAY, TUESDAY'),

)
MEMBERSHIP_TYPE_NAME_CHOICES = (
    ('1 - MONTH', '1 - MONTH'),
    ('2 - MONTH', '2 - MONTH'),
    ('3 - MONTH', '3 - MONTH'),
    ('6 - MONTH', '6 - MONTH'),
    ('1 - YEAR', '1 - YEAR'),
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class USER(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(max_length=30, null=False, blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.get_full_name()


class Member(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Coach(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='coach_member')
    identity_card = models.ImageField(upload_to='identity_card', null=False, blank=False)
    address = models.CharField(max_length=30, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    country = models.CharField(max_length=30, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.member.first_name


class Shift(models.Model):
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    days_of_week = models.CharField(max_length=100, choices=DAYS_OF_WEEK_CHOICES, null=False, blank=False)

    def __str__(self):
        return self.days_of_week


class CoachShift(models.Model):
    coach = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='Member_shifts')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='shift_coaches')

    def __str__(self):
        return self.coach.user.username


class MembershipType(models.Model):
    name = models.CharField(max_length=100, choices=MEMBERSHIP_TYPE_NAME_CHOICES, null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False, )
    price = models.IntegerField(null=False, blank=False)

    def save(self, *args, **kwargs):
        if self.name == '1 - MONTH':
            self.duration = 30
        elif self.name == '2 - MONTH':
            self.duration = 60
        elif self.name == '3 - MONTH':
            self.duration = 90
        elif self.name == '6 - MONTH':
            self.duration = 180
        elif self.name == '1 - YEAR':
            self.duration = 365

        super().save(*args, **kwargs)

    def duration_in_sets(self):
        return str(self.duration) + ' SETS'

    def __str__(self):
        return self.name


class InMemberShip(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_in_membership')
    membership = models.ForeignKey(MembershipType, on_delete=models.CASCADE, related_name='membership_member')
    start_date = models.DateField(auto_now=True, auto_now_add=False, null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    sets_remaining = models.IntegerField(null=True, blank=True)
    checkin_count = models.IntegerField(default=0, null=False, blank=True)
    checkin_datetime = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        membership_durations = {
            "1 - MONTH": 30,
            "2 - MONTH": 60,
            "3 - MONTH": 90,
            "6 - MONTH": 180,
            "1 - YEAR": 365
        }

        if self.membership.name in membership_durations:
            if self.sets_remaining is None:
                self.sets_remaining = membership_durations[self.membership.name]
            if self.start_date is None:
                self.start_date = date.today()
            self.end_date = self.start_date + timedelta(days=membership_durations[self.membership.name])

        super(InMemberShip, self).save(*args, **kwargs)

    def check_in(self):
        if self.sets_remaining is not None and self.sets_remaining > 0:
            self.sets_remaining -= 1
            self.checkin_count += 1
            self.save()
            checkin = CheckIn(membership=self)
            checkin.save()
        elif self.sets_remaining == 0:
            return "Sorry, you have no more sets remaining."
        else:
            return "Sets remaining is not defined."

    def get_checkin_times(self):
        return self.checkins.values_list('checkin_datetime', flat=True)

    def __str__(self):
        return self.member.first_name + '   -   ' + self.membership.name


class CheckIn(models.Model):
    membership = models.ForeignKey(InMemberShip, on_delete=models.CASCADE, related_name='checkins')
    checkin_datetime = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(CheckIn, self).save(*args, **kwargs)
        self.membership.checkin_count = self.membership.checkins.count()
        self.membership.save()

    def __str__(self):
        return self.membership.member.first_name + '   -   ' + self.membership.membership.name + '   -   ' + str(
            self.checkin_datetime)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
