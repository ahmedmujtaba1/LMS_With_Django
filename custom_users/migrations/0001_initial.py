# Generated by Django 4.2.3 on 2023-07-16 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('vil', models.FloatField()),
                ('aul', models.FloatField()),
                ('kl', models.FloatField()),
                ('vel', models.FloatField()),
                ('anl', models.FloatField()),
                ('sl', models.FloatField()),
                ('sol', models.FloatField()),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Q1', models.CharField(max_length=20)),
                ('Q2', models.CharField(max_length=20)),
                ('Q3', models.CharField(max_length=20)),
                ('Q4', models.CharField(max_length=20)),
                ('Q5', models.CharField(max_length=20)),
                ('Q6', models.CharField(max_length=20)),
                ('Q7', models.CharField(max_length=20)),
                ('Q8', models.CharField(max_length=20)),
                ('Q9', models.CharField(max_length=20)),
                ('Q10', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Response',
                'verbose_name_plural': 'Responses',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_name', models.CharField(max_length=250)),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('contact_no', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
