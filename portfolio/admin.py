from django.contrib import admin
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Experience, Certification, Skill, ContactMessage, VisitorLog, PageView, ClickEvent, SectionView, DevToolsEvent


@receiver(user_logged_in)
def notify_admin_login(sender, request, user, **kwargs):
    try:
        ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR', 'Unknown')
        ua = request.META.get('HTTP_USER_AGENT', 'Unknown')
        referer = request.META.get('HTTP_REFERER', 'Direct')
        from django.utils import timezone
        time = timezone.now().strftime('%d %b %Y, %I:%M %p')

        send_mail(
            subject=f'[Portfolio Alert] Admin Login Detected',
            message=f"""
Someone just logged into your portfolio admin panel.

─────────────────────────────────
  Username  : {user.username}
  Time      : {time} (UTC)
  IP Address: {ip}
  Browser   : {ua[:200]}
  Referrer  : {referer}
─────────────────────────────────

If this was not you, change your password immediately at:
https://www.ikramhamid.in/admin/password_change/

─────────────────────────────────
Portfolio Admin Alert System
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
            fail_silently=True,
        )
    except Exception as e:
        print(f"[ADMIN LOGIN EMAIL ERROR] {e}")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'order']
    list_editable = ['featured', 'order']
    search_fields = ['title', 'description']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'company', 'start_date', 'end_date', 'order']
    list_editable = ['order']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display  = ['title', 'issuer', 'date', 'has_image']
    search_fields = ['title', 'issuer']

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Image'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency']
    list_filter  = ['category']
    list_editable = ['proficiency']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'sent_at']
    readonly_fields = ['sent_at']


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'country', 'city', 'device_type', 'browser', 'page_views', 'total_time_sec', 'first_seen']
    list_filter  = ['device_type', 'country']
    search_fields = ['ip_address', 'country', 'city', 'browser']
    readonly_fields = ['session_key', 'first_seen', 'last_seen']


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['visitor', 'path', 'viewed_at']
    readonly_fields = ['viewed_at']


@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ['visitor', 'element', 'element_type', 'section', 'clicked_at']
    readonly_fields = ['clicked_at']


@admin.register(SectionView)
class SectionViewAdmin(admin.ModelAdmin):
    list_display = ['visitor', 'section', 'time_spent', 'entered_at']
    readonly_fields = ['entered_at']


@admin.register(DevToolsEvent)
class DevToolsEventAdmin(admin.ModelAdmin):
    list_display = ['visitor', 'method', 'opened_at']
    readonly_fields = ['opened_at']