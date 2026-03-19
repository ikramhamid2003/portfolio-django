from django.contrib import admin
from .models import Project, Experience, Certification, Skill, ContactMessage


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
    list_display = ['title', 'issuer', 'date']
    search_fields = ['title', 'issuer']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency']
    list_filter = ['category']
    list_editable = ['proficiency']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'sent_at']
    readonly_fields = ['sent_at']


from .models import VisitorLog, PageView

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
