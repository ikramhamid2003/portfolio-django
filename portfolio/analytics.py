import requests
import hashlib
from user_agents import parse as ua_parse
from .models import VisitorLog, PageView


def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def get_geo(ip):
    """Free ip-api.com — no key needed, 1000 req/min."""
    if ip in ('127.0.0.1', 'localhost', '::1'):
        return {}
    try:
        r = requests.get(
            f'http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,lat,lon',
            timeout=3
        )
        data = r.json()
        if data.get('status') == 'success':
            return {
                'country':      data.get('country', ''),
                'country_code': data.get('countryCode', ''),
                'city':         data.get('city', ''),
                'region':       data.get('regionName', ''),
                'latitude':     data.get('lat'),
                'longitude':    data.get('lon'),
            }
    except Exception:
        pass
    return {}


def session_key(request, ip):
    raw = f"{ip}-{request.META.get('HTTP_USER_AGENT','')}"
    return hashlib.sha256(raw.encode()).hexdigest()[:48]


def track_visit(request):
    """Call this from the index view. Returns the VisitorLog instance."""
    ip  = get_client_ip(request)
    ua_str = request.META.get('HTTP_USER_AGENT', '')
    ua  = ua_parse(ua_str)

    if ua.is_bot:
        return None

    skey = session_key(request, ip)

    visitor, created = VisitorLog.objects.get_or_create(
        session_key=skey,
        defaults={
            'ip_address': ip,
            'user_agent': ua_str,
            'browser':    f"{ua.browser.family} {ua.browser.version_string}",
            'os':         f"{ua.os.family} {ua.os.version_string}",
            'device_type': 'mobile' if ua.is_mobile else ('tablet' if ua.is_tablet else 'desktop'),
            'referrer':   request.META.get('HTTP_REFERER', ''),
            'is_bot':     ua.is_bot,
        }
    )

    if created:
        geo = get_geo(ip)
        for k, v in geo.items():
            setattr(visitor, k, v)
        visitor.save()
    else:
        visitor.page_views += 1
        visitor.save(update_fields=['page_views', 'last_seen'])

    PageView.objects.create(
        visitor=visitor,
        path=request.path,
        section=request.GET.get('section', ''),
    )
    return visitor
