# Generated by Django 3.2.19 on 2023-08-02 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosticAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=100, unique=True)),
                ('field', models.CharField(blank=True, choices=[('Web Development', 'Web Development'), ('Hardware', 'Hardware'), ('AI', 'AI')], max_length=200)),
                ('admin', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Supervisor',
                'verbose_name_plural': 'Supervisors (Make supervisors)',
            },
        ),
        migrations.CreateModel(
            name='NewProjectGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supervisor', models.TextField(blank=True, null=True)),
                ('student1', models.TextField(blank=True, null=True)),
                ('student2', models.TextField(blank=True, null=True)),
                ('student3', models.TextField(blank=True, null=True)),
                ('prediction', models.TextField(blank=True, null=True)),
                ('notice', models.TextField(blank=True, null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('upload_file', models.FileField(null=True, upload_to='uploads/')),
                ('approved', models.BooleanField(default=False, null=True)),
            ],
            options={
                'verbose_name': 'Project Group',
                'verbose_name_plural': 'Project Groups',
                'db_table': 'new_project_group',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProjectUploads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=150, null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('upload_file', models.FileField(upload_to='uploads/')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Project Proposal',
                'verbose_name_plural': 'Project Proposals',
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=100, unique=True)),
                ('admin', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 1: How do you prefer to learn?')),
                ('question2', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 2: Which learning style suits you best?')),
                ('question3', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 3: What is your preferred learning method?')),
                ('question4', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 4: Which learning environment do you find most effective?')),
                ('question5', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 5: How do you like to process information?')),
                ('question6', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 6: Which learning approach resonates with you?')),
                ('question7', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 7: What type of learner are you?')),
                ('question8', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 8: How do you prefer to study or revise?')),
                ('question9', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 9: Which learning style feels most natural to you?')),
                ('question10', models.CharField(blank=True, choices=[('visual', 'Visual Learner'), ('aural', 'Aural Learner'), ('kinesthetic', 'Kinesthetic Learner'), ('verbal', 'Verbal Learner'), ('analytical', 'Analytical Learner'), ('social', 'Social Learner'), ('solitary', 'Solitary Learner')], max_length=200, null=True, verbose_name='Question 10: How do you engage with new information?')),
                ('prediction', models.CharField(blank=True, choices=[('Hardware', 'Hardware'), ('Web Development', 'Web Development'), ('AI', 'AI')], max_length=200)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'Questionnaire',
                'verbose_name_plural': 'All Questionnaire',
            },
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('topic', models.CharField(blank=True, max_length=250, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('notice', models.TextField(blank=True, null=True)),
                ('student1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_student1', to='diagnostic_centers.students')),
                ('student2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_student2', to='diagnostic_centers.students')),
                ('student3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_student3', to='diagnostic_centers.students')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_supervisor', to='diagnostic_centers.diagnosticadmin')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
    ]
