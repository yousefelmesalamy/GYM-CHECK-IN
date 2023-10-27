from django.contrib import admin
from .models import USER, Coach, Shift, CoachShift, MembershipType, InMemberShip, CheckIn, Member
from django.utils.html import format_html


# Register your models here.


class USERAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['username', 'email', 'phone_number', 'password', ('first_name', 'last_name')]}),
        ("Permissions",
         {
             "classes": ["collapse"],
             "fields": ('is_staff', 'is_active', 'is_superuser')})]

    list_display = (
        'colored_username_of_superuser_only', 'get_full_name', 'phone_number', 'email', 'is_staff',
        'is_active', 'is_superuser', 'last_login',
        'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    list_display_links = ('colored_username_of_superuser_only', 'email', 'phone_number',)
    search_fields = ('username', 'email')
    ordering = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')
    empty_value_display = "EMPTY OR DISABLED BY ADMIN"

    def colored_username_of_superuser_only(self, obj):
        if obj.is_superuser:
            return format_html('<span style="color: #{};">{}</span>', 'FF0000', obj.username)
        return obj.username

    colored_username_of_superuser_only.admin_order_field = 'username'
    colored_username_of_superuser_only.short_description = 'SuperUsers'


class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    list_filter = ('first_name', 'last_name', 'phone_number')
    list_display_links = ('first_name', 'last_name', 'phone_number')
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('first_name', 'last_name', 'phone_number')
    empty_value_display = "EMPTY OR DISABLED BY ADMIN"


class CoachAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['member', 'address', 'city', 'country', 'date_of_birth']})
        , ('Identity Card', {'fields': ['identity_card']})]

    list_display = ('member', 'address', 'city', 'country', 'date_of_birth', 'preview_identity_card')
    list_filter = ('member', 'address', 'city', 'country', 'date_of_birth')
    list_display_links = ('member', 'address', 'city', 'country', 'date_of_birth',)
    search_fields = ('member', 'address', 'city', 'country', 'date_of_birth')
    ordering = ('member', 'address', 'city', 'country', 'date_of_birth')
    empty_value_display = "NOT STAFF OR DISABLED BY ADMIN"

    def preview_identity_card(self, obj):
        return format_html('<img src="{}" width="180" height="100"/>'.format(obj.identity_card.url))

    preview_identity_card.short_description = 'Identity Card'


class ShiftAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Shift', {'fields': ['start_time', 'end_time', 'days_of_week']})]

    list_display = ('days_of_week', 'start_time', 'end_time',)
    list_filter = ('start_time', 'end_time', 'days_of_week')
    list_display_links = ('start_time', 'end_time', 'days_of_week')
    search_fields = ('start_time', 'end_time', 'days_of_week')
    ordering = ('start_time', 'end_time', 'days_of_week')
    empty_value_display = "EMPTY OR DISABLED BY ADMIN"


class CoachShiftAdmin(admin.ModelAdmin):
    fieldsets = [
        ('CoachShift', {'fields': ['coach', 'shift']})]

    list_display = ('coach', 'shift',)
    list_filter = ('coach', 'shift')
    list_display_links = ('coach', 'shift')
    ordering = ('coach', 'shift')
    empty_value_display = "EMPTY OR DISABLED BY ADMIN"


class MembershipTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('MembershipType', {'fields': ['name', 'price', 'duration']})]

    list_display = ('name', 'price', 'duration_in_sets',)
    list_filter = ('name', 'price', 'duration',)
    list_display_links = ('name', 'price',)
    search_fields = ('name', 'price', 'duration',)
    ordering = ('name', 'price', 'duration',)
    empty_value_display = "EMPTY OR DISABLED BY ADMIN"
    readonly_fields = ['duration', ]

    def duration_in_sets(self, obj):
        return obj.duration_in_sets()

    duration_in_sets.admin_order_field = 'duration'

    duration_in_sets.short_description = 'Duration in Sets'


class InMemberShipAdmin(admin.ModelAdmin):
    fieldsets = [
        ('InMemberShip', {'fields': ['member', 'membership', 'sets_remaining', 'checkin_count']})
        , ('Date', {'fields': ['end_date', ]})
    ]

    list_display = ('member', 'membership', 'sets_remaining', 'checkin_count', 'start_date', 'end_date')
    list_filter = ('member', 'membership', 'sets_remaining', 'checkin_count', 'start_date', 'end_date')
    list_display_links = ('member', 'membership', 'sets_remaining', 'checkin_count',)
    search_fields = ('member', 'membership', 'sets_remaining', 'checkin_count', 'start_date', 'end_date')
    ordering = ('member', 'membership', 'sets_remaining', 'checkin_count', 'start_date', 'end_date')
    # readonly_fields = ['sets_remaining', ]
    empty_value_display = "EMPTY OR DISABLED BY ADMIN"


class CheckInAdminSite(admin.ModelAdmin):
    fieldsets = [
        ("MEMBERSHIPS", {'fields': ['membership']}),
        ("CHECK IN DATES", {'fields': ['checkin_datetime']}),
    ]
    list_display = ('membership', 'checkin_datetime')
    list_filter = ('membership', 'checkin_datetime')
    list_display_links = ('membership', 'checkin_datetime')
    search_fields = ('membership', 'checkin_datetime')
    ordering = ('membership', 'checkin_datetime')
    readonly_fields = ['checkin_datetime', ]


admin.site.register(USER, USERAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(CoachShift, CoachShiftAdmin)
admin.site.register(MembershipType, MembershipTypeAdmin)
admin.site.register(InMemberShip, InMemberShipAdmin)
admin.site.register(CheckIn, CheckInAdminSite)
