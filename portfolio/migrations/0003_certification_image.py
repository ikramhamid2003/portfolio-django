from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_visitorlog_pageview'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='certifications/'),
        ),
    ]