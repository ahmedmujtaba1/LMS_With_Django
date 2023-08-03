from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd
from django.db import models
from django.db import models
from collections import Counter
import re
from django.db import models

class Students(models.Model):
    id = models.CharField(max_length = 50, primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=20, unique=True, blank=False)
    password = models.CharField(max_length=100, unique=True,  blank=False)
    admin = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Students'
    def __str__(self):
        return self.username

FIELD_CHOICES = [
        ('Web Development', 'Web Development'),
        ('Hardware', 'Hardware'),
        ('AI', 'AI'),
    ]


class DiagnosticAdmin(models.Model):
    username = models.CharField(max_length=20, unique=True, blank=False)
    password = models.CharField(max_length=100, unique=True, blank=False)
    field = models.CharField(max_length=200, choices=FIELD_CHOICES, blank=True)
    admin = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Supervisor'
        verbose_name_plural = 'Supervisors (Make supervisors)'

    def __str__(self):
        return f"{self.username} - {self.field}"
    
     
###########################################################################################################################3
class Groups(models.Model):
    name = models.CharField(max_length=250, blank=False)
    topic = models.CharField(max_length=250, blank=True, null=True)
    student1 = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='group_student1', null=True)
    student2 = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='group_student2', null=True)
    student3 = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='group_student3', null=True)
    supervisor = models.ForeignKey(DiagnosticAdmin, on_delete=models.CASCADE, related_name='group_supervisor', null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    notice = models.TextField(blank=True, null=True) 
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name



class Questionnaire(models.Model):
    LEARNING_STYLE_CHOICES = (
        ('visual', 'Visual Learner'),
        ('aural', 'Aural Learner'),
        ('kinesthetic', 'Kinesthetic Learner'),
        ('verbal', 'Verbal Learner'),
        ('analytical', 'Analytical Learner'),
        ('social', 'Social Learner'),
        ('solitary', 'Solitary Learner'),
    )

    PREDICTION_CHOICES = (
    ('Hardware', 'Hardware'),
    ('Web Development', 'Web Development'),
    ('AI', 'AI'),

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,  unique=True)
    question1 = models.CharField(
        verbose_name='Question 1: How do you prefer to learn?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )
    question2 = models.CharField(
        verbose_name='Question 2: Which learning style suits you best?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )
    question3 = models.CharField(
        verbose_name='Question 3: What is your preferred learning method?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )
    question4 = models.CharField(
        verbose_name='Question 4: Which learning environment do you find most effective?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )
    question5 = models.CharField(
        verbose_name='Question 5: How do you like to process information?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )
    question6 = models.CharField(
        verbose_name='Question 6: Which learning approach resonates with you?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )
    question7 = models.CharField(
        verbose_name='Question 7: What type of learner are you?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )
    question8 = models.CharField(
        verbose_name='Question 8: How do you prefer to study or revise?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )
    question9 = models.CharField(
        verbose_name='Question 9: Which learning style feels most natural to you?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )
    question10 = models.CharField(
        verbose_name='Question 10: How do you engage with new information?',
        max_length=200,
        choices=LEARNING_STYLE_CHOICES,
        null=True,
        blank=True
    )

    prediction = models.CharField(max_length=200, choices=PREDICTION_CHOICES, blank=True)
    
    class Meta:
        verbose_name = 'Questionnaire'
        verbose_name_plural = 'All Questionnaire'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Get the data for the current user
        data = Questionnaire.objects.filter(user_id=self.user_id).values()
        df = pd.DataFrame.from_records(data)
        df['other_columns'] = df.drop(['user_id'], axis=1).apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        df_list = df['other_columns'].values.tolist()
        text = ''.join(df_list)
        text = re.sub(',', '', text)
        words = text.split()
        word_counts = Counter(words)
        most_common_word = word_counts.most_common(1)[0][0].lower()

        # Set the prediction field based on the most common word
        if most_common_word == "kinesthetic":
            self.prediction = "Hardware"
        elif most_common_word == "visual":
            self.prediction = "Web Development"
        elif most_common_word == "aural":
            self.prediction = "AI"
        elif most_common_word == "verbal":
            self.prediction = "Web Development"
        elif most_common_word == "social":
            self.prediction = "Web Development"
        elif most_common_word == "solitary":
            self.prediction = "AI"
        elif most_common_word == "analytical":
            self.prediction = "AI"

        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.user)} -{str(self.prediction)} "
    
###################################################################################

from custom_users.models import Profile
class NewProjectGroup(models.Model):
    supervisor = models.TextField(blank=True, null=True)
    student1 = models.TextField(blank=True, null=True)
    student2 = models.TextField(blank=True, null=True)
    student3 = models.TextField(blank=True, null=True)
    prediction = models.TextField(blank=True, null=True)
    notice = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100, null=True)
    upload_file = models.FileField(upload_to='uploads/', null=True)
    approved = models.BooleanField(default=False, null=True)

    class Meta:
        managed = True
        db_table = 'new_project_group'
        verbose_name = 'Project Group'
        verbose_name_plural = 'Project Groups'


    def __str__(self):
        return f"{str(self.supervisor)} - [{str(self.student1)},{str(self.student2)},{str(self.student3)}]"

class ProjectUploads(models.Model):
    #project_stuff = models.ForeignKey(NewProjectGroup, on_delete=models.CASCADE, verbose_name="Supervisor", null=True, blank=True)
    user = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    upload_file = models.FileField(upload_to='uploads/')
    remarks = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Project Proposal'
        verbose_name_plural = 'Project Proposals'
    def __str__(self):
        return self.title
    

# Visual Learner: Web Development
# Aural Learner: AI
# Kinesthetic Learner: Hardware
# Verbal Learner: Web Development
# Analytical Learner: AI
# Social Learner: Web Development
# Solitary Learner: AI
