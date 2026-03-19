from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_certification_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('element', models.CharField(max_length=200)),
                ('element_type', models.CharField(max_length=50)),
                ('target_url', models.TextField(blank=True)),
                ('section', models.CharField(blank=True, max_length=100)),
                ('x_percent', models.FloatField(default=0)),
                ('y_percent', models.FloatField(default=0)),
                ('clicked_at', models.DateTimeField(auto_now_add=True)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clicks', to='portfolio.visitorlog')),
            ],
            options={'ordering': ['-clicked_at']},
        ),
        migrations.CreateModel(
            name='SectionView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('section', models.CharField(max_length=100)),
                ('time_spent', models.IntegerField(default=0)),
                ('entered_at', models.DateTimeField(auto_now_add=True)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_views', to='portfolio.visitorlog')),
            ],
            options={'ordering': ['-entered_at']},
        ),
        migrations.CreateModel(
            name='DevToolsEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('opened_at', models.DateTimeField(auto_now_add=True)),
                ('method', models.CharField(blank=True, max_length=50)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devtools', to='portfolio.visitorlog')),
            ],
            options={'ordering': ['-opened_at']},
        ),
    ]