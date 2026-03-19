from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image_emoji = models.CharField(max_length=10, default='🚀')
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',')]


class Experience(models.Model):
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.role} @ {self.company}"

    def get_bullets(self):
        return [b.strip() for b in self.description.split('\n') if b.strip()]


class Certification(models.Model):
    title = models.CharField(max_length=300)
    issuer = models.CharField(max_length=200)
    date = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    icon_emoji = models.CharField(max_length=10, default='🏆')
    image = models.ImageField(upload_to='certifications/', blank=True, null=True)

    def __str__(self):
        return self.title


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('languages', 'Languages'),
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('ai_ml', 'AI / ML'),
        ('databases', 'Databases'),
        ('tools', 'Tools'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(default=80)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.subject}"


class VisitorLog(models.Model):
    DEVICE_CHOICES = [
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('bot', 'Bot'),
    ]
    session_key    = models.CharField(max_length=64, db_index=True)
    ip_address     = models.GenericIPAddressField(null=True, blank=True)
    country        = models.CharField(max_length=100, blank=True)
    country_code   = models.CharField(max_length=5, blank=True)
    city           = models.CharField(max_length=100, blank=True)
    region         = models.CharField(max_length=100, blank=True)
    latitude       = models.FloatField(null=True, blank=True)
    longitude      = models.FloatField(null=True, blank=True)
    device_type    = models.CharField(max_length=20, choices=DEVICE_CHOICES, default='desktop')
    browser        = models.CharField(max_length=100, blank=True)
    os             = models.CharField(max_length=100, blank=True)
    user_agent     = models.TextField(blank=True)
    referrer       = models.TextField(blank=True)
    first_seen     = models.DateTimeField(auto_now_add=True)
    last_seen      = models.DateTimeField(auto_now=True)
    total_time_sec = models.IntegerField(default=0)
    page_views     = models.IntegerField(default=1)
    is_bot         = models.BooleanField(default=False)

    class Meta:
        ordering = ['-first_seen']

    def __str__(self):
        return f"{self.ip_address} — {self.country} [{self.first_seen:%Y-%m-%d %H:%M}]"

    @property
    def time_spent_display(self):
        s = self.total_time_sec
        if s < 60:
            return f"{s}s"
        elif s < 3600:
            return f"{s // 60}m {s % 60}s"
        else:
            return f"{s // 3600}h {(s % 3600) // 60}m"


class PageView(models.Model):
    visitor      = models.ForeignKey(VisitorLog, on_delete=models.CASCADE, related_name='views')
    path         = models.CharField(max_length=500)
    section      = models.CharField(max_length=100, blank=True)
    viewed_at    = models.DateTimeField(auto_now_add=True)
    time_on_page = models.IntegerField(default=0)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.visitor.ip_address} → {self.path}"


class ClickEvent(models.Model):
    visitor      = models.ForeignKey(VisitorLog, on_delete=models.CASCADE, related_name='clicks')
    element      = models.CharField(max_length=200)
    element_type = models.CharField(max_length=50)
    target_url   = models.TextField(blank=True)
    section      = models.CharField(max_length=100, blank=True)
    x_percent    = models.FloatField(default=0)
    y_percent    = models.FloatField(default=0)
    clicked_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-clicked_at']

    def __str__(self):
        return f"{self.visitor.ip_address} clicked {self.element}"


class SectionView(models.Model):
    visitor    = models.ForeignKey(VisitorLog, on_delete=models.CASCADE, related_name='section_views')
    section    = models.CharField(max_length=100)
    time_spent = models.IntegerField(default=0)
    entered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-entered_at']

    def __str__(self):
        return f"{self.visitor.ip_address} viewed {self.section}"


class DevToolsEvent(models.Model):
    visitor   = models.ForeignKey(VisitorLog, on_delete=models.CASCADE, related_name='devtools')
    opened_at = models.DateTimeField(auto_now_add=True)
    method    = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-opened_at']

    def __str__(self):
        return f"{self.visitor.ip_address} opened devtools via {self.method}"