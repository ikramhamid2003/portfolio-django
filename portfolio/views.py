from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from .models import Project, Experience, Certification, Skill, ContactMessage, VisitorLog, PageView, ClickEvent, SectionView, DevToolsEvent
from .analytics import track_visit
import json


def index(request):
    track_visit(request)
    projects       = Project.objects.all()
    experiences    = Experience.objects.all()
    certifications = Certification.objects.all()
    skills         = Skill.objects.all()
    skill_categories = {}
    for skill in skills:
        cat = skill.get_category_display()
        if cat not in skill_categories:
            skill_categories[cat] = []
        skill_categories[cat].append(skill)
    context = {
        'projects':          projects,
        'featured_projects': projects.filter(featured=True),
        'experiences':       experiences,
        'certifications':    certifications,
        'skill_categories':  skill_categories,
    }
    return render(request, 'portfolio/index.html', context)


def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and subject and message:
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            try:
                email_body = f"""
New contact form submission from your portfolio.

Name    : {name}
Email   : {email}
Subject : {subject}

Message:
{message}

---
Sent via portfolio contact form
"""
                send_mail(
                    subject=f"[Portfolio] {subject} — from {name}",
                    message=email_body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                    fail_silently=False,
                )
                mail_sent = True
            except Exception as e:
                mail_sent = False
                print(f"[EMAIL ERROR] {e}")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Message sent!'})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'All fields are required.'})
        return redirect('/')
    return redirect('/')


def track_time(request):
    if request.method == 'POST':
        from .analytics import session_key, get_client_ip
        try:
            data    = json.loads(request.body)
            seconds = int(data.get('seconds', 0))
            ip      = get_client_ip(request)
            skey    = session_key(request, ip)
            VisitorLog.objects.filter(session_key=skey).update(total_time_sec=seconds)
            return JsonResponse({'ok': True})
        except Exception:
            pass
    return JsonResponse({'ok': False})


def track_event(request):
    if request.method == 'POST':
        from .analytics import session_key, get_client_ip
        try:
            data       = json.loads(request.body)
            ip         = get_client_ip(request)
            skey       = session_key(request, ip)
            visitor    = VisitorLog.objects.filter(session_key=skey).first()
            if not visitor:
                return JsonResponse({'ok': False})
            event_type = data.get('type')
            if event_type == 'click':
                ClickEvent.objects.create(
                    visitor      = visitor,
                    element      = data.get('element', '')[:200],
                    element_type = data.get('element_type', '')[:50],
                    target_url   = data.get('target_url', ''),
                    section      = data.get('section', '')[:100],
                    x_percent    = float(data.get('x_percent', 0)),
                    y_percent    = float(data.get('y_percent', 0)),
                )
            elif event_type == 'section':
                SectionView.objects.create(
                    visitor    = visitor,
                    section    = data.get('section', '')[:100],
                    time_spent = int(data.get('time_spent', 0)),
                )
            elif event_type == 'devtools':
                DevToolsEvent.objects.create(
                    visitor = visitor,
                    method  = data.get('method', '')[:50],
                )
            return JsonResponse({'ok': True})
        except Exception as e:
            print(f"[TRACK EVENT ERROR] {e}")
    return JsonResponse({'ok': False})


@staff_member_required
def analytics_dashboard(request):
    now   = timezone.now()
    day30 = now - timedelta(days=30)
    day7  = now - timedelta(days=7)
    visitors = VisitorLog.objects.filter(is_bot=False)
    total_visitors = visitors.count()
    last30         = visitors.filter(first_seen__gte=day30).count()
    last7          = visitors.filter(first_seen__gte=day7).count()
    avg_time       = visitors.aggregate(a=Avg('total_time_sec'))['a'] or 0
    total_views    = visitors.aggregate(s=Sum('page_views'))['s'] or 0
    by_country     = visitors.values('country', 'country_code').annotate(n=Count('id')).order_by('-n')[:15]
    by_device      = visitors.values('device_type').annotate(n=Count('id')).order_by('-n')
    by_browser     = visitors.values('browser').annotate(n=Count('id')).order_by('-n')[:10]
    by_os          = visitors.values('os').annotate(n=Count('id')).order_by('-n')[:10]
    daily = []
    for i in range(13, -1, -1):
        d = now - timedelta(days=i)
        daily.append({'date': d.strftime('%b %d'), 'count': visitors.filter(first_seen__date=d.date()).count()})
    recent_list    = visitors.order_by('-first_seen')[:50]
    contacts       = ContactMessage.objects.order_by('-sent_at')[:20]
    top_clicks     = ClickEvent.objects.values('element', 'element_type', 'section').annotate(n=Count('id')).order_by('-n')[:20]
    top_sections   = SectionView.objects.values('section').annotate(n=Count('id'), avg_time=Avg('time_spent')).order_by('-n')
    devtools_count = DevToolsEvent.objects.count()
    recent_clicks  = ClickEvent.objects.select_related('visitor').order_by('-clicked_at')[:30]
    ctx = {
        'total_visitors': total_visitors, 'last30': last30, 'last7': last7,
        'avg_time': int(avg_time), 'total_views': total_views,
        'by_country': by_country, 'by_device': by_device,
        'by_browser': by_browser, 'by_os': by_os,
        'daily': daily, 'recent_list': recent_list, 'contacts': contacts,
        'top_clicks': top_clicks, 'top_sections': top_sections,
        'devtools_count': devtools_count, 'recent_clicks': recent_clicks,
    }
    return render(request, 'portfolio/analytics.html', ctx)