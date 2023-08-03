from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import DiagnosticAdmin, Students, Questionnaire
from .forms import AdminLoginForm, StaffLoginForm
from .forms import GroupsForm
def search_paginator(request):
    Centers = Students.objects.all()

    query = request.GET.get('q')
    if query:
        Centers = Centers.filter(
            Q(name__icontains=query) |
            Q(website__icontains=query)
        )
        print(Centers)

    paginator = Paginator(Centers, 12)
    page = request.GET.get('page')
    all_centers = paginator.get_page(page)

    context = {'Centers': all_centers,}
    template_name = 'diagnostic_centers/all_centers.html'

    return render(request, template_name, context)


def admin_login(request):
    import pandas as pd
    from random import sample
    from .models import DiagnosticAdmin, Questionnaire, Groups
    import logging
    def fetch_records():
        students = list(Questionnaire.objects.all().order_by('prediction'))
        num_students = len(students)
        groups = []

        supervisor_fields_and_names = list(DiagnosticAdmin.objects.values_list('field', 'username').distinct())

        supervisors_by_field = {}
        for supervisor_field, supervisor_name in supervisor_fields_and_names:
            key = (supervisor_field, supervisor_name)
            supervisors_by_field[key] = []

        for student in students:
            student_field = student.prediction
            for supervisor_field, supervisor_name in supervisor_fields_and_names:
                if supervisor_field in student_field:
                    key = (supervisor_field, supervisor_name)
                    supervisors_by_field[key].append(student)
                    break

        print("Supervisor Dic : ", supervisors_by_field)

        for key, supervisor_students in supervisors_by_field.items():
            supervisor_field, supervisor_name = key
            num_supervisor_students = len(supervisor_students)
            num_groups = (num_supervisor_students + 2) // 3
            for i in range(num_groups):
                group_students = supervisor_students[i * 3: (i + 1) * 3]
                group = {
                    # 'Supervisor Field': supervisor_field,
                    'Supervisor': supervisor_name,
                    'Students': [student.user for student in group_students],
                    'Predictions': [student.prediction for student in group_students]
                }
                groups.append(group)

        return groups



    record_groups = fetch_records()
    df = pd.DataFrame(record_groups)
    print(df)

    import sqlite3
    import pandas as pd

    conn = sqlite3.connect('db.sqlite3')

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS new_project_group (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supervisor TEXT,
            student1 TEXT,
            student2 TEXT,
            student3 TEXT,
            prediction TEXT
        )
    '''
    conn.execute(create_table_query)
    num = 0
    for _, row in df.iterrows():
        supervisor = row['Supervisor']
        
        try:
            student1 = str(row['Students'][0])
        except:student1 = ''

        try:
            student2 = str(row['Students'][1])
        except:student2 = ""
        try:
            student3 = str(row['Students'][2])
        except:student3 = ''

        predictions = ', '.join(row['Predictions'])

        select_query = '''
            SELECT COUNT(*) FROM new_project_group
            WHERE supervisor = ? AND student1 = ? AND student2 = ? AND student3 = ? AND prediction = ? AND approved= ?
        '''
        
        try:
            duplicate_check = conn.execute(select_query, (supervisor, student1, student2, student3, predictions, False)).fetchone()[0]
        except:pass

        if duplicate_check == 0:  
            insert_query = '''
                INSERT INTO new_project_group (supervisor, student1, student2, student3, prediction, approved)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            conn.execute(insert_query, (supervisor, student1, student2, student3, predictions, False))
            num += 3
            print("Record inserted successfully.")

    conn.commit()
    conn.close()

    admin_login_form = AdminLoginForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            DiagnosticAdmin.objects.get(username=username, password=password)
            return redirect('diagnostic_centers:admin-dashboard', username)

        except DiagnosticAdmin.DoesNotExist:
            return redirect('diagnostic_centers:admin-login')

    template = 'diagnostic_centers/admin_login.html'

    context = {'admin_login_form': admin_login_form}

    return render(request, template, context)


################################################################################################################

def admin_dashboard(request, username=None):
    project_uploads = ProjectUploads.objects.all()#filter(project_stuff__supervisor=request.user.newprojectgroup)
    #return render(request, 'project_list.html', {'project_uploads': project_uploads})
    admin2 = DiagnosticAdmin.objects.get(username=username)
    new_groups = NewProjectGroup.objects.all()
    if request.method == 'POST':
        form = GroupsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = GroupsForm()
    admin = DiagnosticAdmin.objects.all()
    page = request.GET.get('page')
    conn = sqlite3.connect('db.sqlite3')
    query = "SELECT * FROM new_project_group"
    fdf = pd.read_sql_query(query, conn)
    df = fdf[fdf.apply(lambda row: username in ' '.join(row.values.astype(str)), axis=1)]
    groups = Groups.objects.all()
    user = request.user.username
    prediction = df["prediction"]
    prediction = str(prediction).split(',')
    prediction = prediction[0]
    prediction = prediction.replace('5','')
    template = ['diagnostic_centers/admin_dashboard.html', 'home.html']
    context = {
        'admin': admin,
        'groups': groups,
        'form': form,
        'admin' : admin,
        'dataframe': df,
        'new_groups':new_groups,
        'admin2': admin2,
        'project_uploads': project_uploads,
        'prediction' : prediction,
    }
    return render(request, template, context)
  

def admin_logout(request):
    messages.success(request, 'Logged Out.', extra_tags='html_safe')
    return redirect('diagnostic_centers:admin-login')

def staff_login(request):
    staff_login_form = StaffLoginForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            Students.objects.get(username=username, password=password)
            return redirect('diagnostic_centers:staff-dashboard', username)
        except Students.DoesNotExist:
            return redirect('diagnostic_centers:staff-login')
    template = 'diagnostic_centers/staff_login.html'
    context = {'staff_login_form': staff_login_form}
    return render(request, template, context)

def staff_dashboard(request, id=None, username=None):
    staff = Students.objects.get(username=username)
    admins = DiagnosticAdmin.objects.filter(staff=staff)
    template = 'diagnostic_centers/staff_dashboard.html'
    context = {
        'staff': staff,
        'admins': admins,
        'staff_username': username,    }
    return render(request, template, context)

def staff_logout(request):
    # messages.success(request, 'Logged Out.', extra_tags='html_safe')
    return redirect('diagnostic_centers:staff-login')

def center_details(request, id=id):
    template = 'diagnostic_centers/center_details.html'
    return render(request, template)

############################################################################################################
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from sklearn.mixture import GaussianMixture
import pandas as pd
import numpy as np
from .models import Groups, Students

#Questionnaire view
def q(request):
    if request.method == 'POST':
        data = request.POST.copy()
        ans = ['A','B','C','D','E','F','G','H','I','J']
        value = [0,0,0,0,0,0,0]
        arr = ['Visual Learner','Aural Learner','Kinesthetic Learner','Verbal Learner','Analytical Learner','Social Learner','Solitary Learner']
        for i,opt in enumerate(arr):
            if data.get('question-1-answers')==opt:
                ans[0] = opt;
                value[i] = value[i] + 1
            if data.get('question-2-answers')==opt:
                ans[1] = opt;
                value[i] = value[i] + 1
            if data.get('question-3-answers')==opt:
                ans[2] = opt;
                value[i] = value[i] + 1
            if data.get('question-4-answers')==opt:
                ans[3] = opt;
                value[i] = value[i] + 1
            if data.get('question-5-answers')==opt:
                ans[4] = opt;
                value[i] = value[i] + 1
            if data.get('question-6-answers')==opt:
                ans[5] = opt;
                value[i] = value[i] + 1
            if data.get('question-7-answers')==opt:
                ans[6] = opt;
                value[i] = value[i] + 1
            if data.get('question-8-answers')==opt:
                ans[7] = opt;
                value[i] = value[i] + 1
            if data.get('question-9-answers')==opt:
                ans[8] = opt;
                value[i] = value[i] + 1
            if data.get('question-10-answers')==opt:
                ans[9] = opt;
                value[i] = value[i] + 1
        user = Students.objects.get(id = data.get('check'))
        result = Response(id = user)
        result.Q1 = ans[0]
        result.Q2 = ans[1]
        result.Q3 = ans[2]
        result.Q4 = ans[3]
        result.Q5 = ans[4]
        result.Q6 = ans[5] 
        result.Q7 = ans[6]
        result.Q8 = ans[7]
        result.Q9 = ans[8]
        result.Q10 = ans[9]
        result.save() #Query to save Response of Student
        re = Answers(id = user)
        re.vil = float(value[0])
        re.aul = float(value[1])
        re.kl = float(value[2])
        re.vel = float(value[3])
        re.anl = float(value[4])
        re.sl = float(value[5])
        re.sol = float(value[6])
        re.save()
        base_url = reverse('Thanks')  
        query_string =  urlencode({'id': data.get('check')})  
        url = '{}?{}'.format(base_url, query_string)  
        return redirect(url)
    else:
        result = request.GET.get('id')
    return render(request,'Q.html', {'id':result})


###############################################################################################

from django.shortcuts import render, redirect
from .forms import QuestionnaireForm

def questionnaire(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            questionnaire.user = request.user
            questionnaire.save()
            return redirect('home')
        else:
            return render(request, "error.html")
    else:
        form = QuestionnaireForm(initial={'user': request.user})
    return render(request, 'questionnaire.html', {'form': form})

#######################################################################

data = Questionnaire.objects.all()
import pandas as pd
from django.db import models
data = Questionnaire.objects.all().values()
df = pd.DataFrame.from_records(data)
df['other_columns'] = df.drop(['user_id'], axis=1).apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
print(df[['id', 'user_id', 'other_columns']])

data = Questionnaire.objects.all()
import pandas as pd

import sqlite3
from collections import Counter
import re

# Fetch the data from the database
data = Questionnaire.objects.all().values()
df = pd.DataFrame.from_records(data)
df['other_columns'] = df.drop(['user_id'], axis=1).apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

for index, row in df.iterrows():
    text = re.sub(',', '', row['other_columns'])
    words = text.split()
    word_counts = Counter(words)
    most_common_word = word_counts.most_common(1)[0][0]

    # Perform further processing based on the prediction
    if most_common_word == "kinesthetic":
        prediction = "Hardware"
    elif most_common_word == "visual":
        prediction = "Web Development"
    elif most_common_word == "aural":
        prediction = "AI"
    elif most_common_word == "verbal":
        prediction = "Web Development"
    elif most_common_word == "social":
        prediction = "Web Development"
    elif most_common_word == "solitary":
        prediction = "AI"
    elif most_common_word == "analytical":
        prediction = "AI"
    else:
        prediction = ""  # Set default value if no match is found

    # Update the prediction in the database for the current user
    user_id = row['user_id']
    cursor.execute("UPDATE diagnostic_centers_questionnaire SET prediction = ? WHERE user_id = ?", (prediction, user_id))
    conn.commit()

# Close the database connection
conn.close()

    
# Visual Learner: Web Development
# Aural Learner: AI
# Kinesthetic Learner: Hardware
# Verbal Learner: Web Development
# Analytical Learner: AI
# Social Learner: Web Development
# Solitary Learner: AI


######################################################################################################
import pandas as pd
from random import sample
from .models import DiagnosticAdmin, Questionnaire, Groups
# def fetch_records():
#     supervisors = list(DiagnosticAdmin.objects.all())
#     students = list(Questionnaire.objects.all().order_by('prediction'))
#     num_students = len(students)
#     num_supervisors = len(supervisors)
#     groups = []

#     for i in range(0, num_students, 3):
#         group_students = students[i:i+3]
#         group_supervisor = supervisors[i // 3 % num_supervisors]
#         group = {
#             'Supervisor': group_supervisor.username,
#             'Students': [student.user for student in group_students],
#             'Predictions': [student.prediction for student in group_students]
#         }
#         groups.append(group)

#     return groups
# record_groups = fetch_records()
# df = pd.DataFrame(record_groups)
# print(df)

import pandas as pd
from random import sample
from .models import DiagnosticAdmin, Questionnaire, Groups

# def fetch_records():
#     supervisors = list(DiagnosticAdmin.objects.all())
#     students = list(Questionnaire.objects.all().order_by('prediction'))
#     num_students = len(students)
#     num_supervisors = len(supervisors)
#     groups = []

#     for i in range(0, num_students, 3):
#         group_students = students[i:i+3]
#         group_supervisor = supervisors[i // 3 % num_supervisors]
        
#         # Check if the supervisor's field matches the student's prediction
#         if group_supervisor.field == group_students[0].prediction:
#             group = {
#                 'Supervisor': group_supervisor.username,
#                 'Students': [student.user for student in group_students],
#                 'Predictions': [student.prediction for student in group_students]
#             }
#             groups.append(group)

#     return groups

# record_groups = fetch_records()
# df = pd.DataFrame(record_groups)
# print(df)

# import pandas as pd
# from random import sample
# from .models import DiagnosticAdmin, Questionnaire, Groups

# def fetch_records():
#     supervisors = list(DiagnosticAdmin.objects.all())
#     students = list(Questionnaire.objects.all().order_by('prediction'))
#     num_students = len(students)
#     num_supervisors = len(supervisors)
#     groups = []

#     # Step size of 3 to create non-overlapping groups of students
#     for i in range(0, num_students, 3):
#         group_students = students[i:i + 3]
#         group_supervisor = supervisors[i // 3 % num_supervisors]
#         group = {
#             'Supervisor': group_supervisor.username,
#             'Students': [student.user for student in group_students],
#             'Predictions': [student.prediction for student in group_students]
#         }
#         groups.append(group)

#     # Handle remaining students
#     remaining_students = num_students % 3
#     if remaining_students:
#         remaining_group_students = students[-remaining_students:]
#         remaining_group_supervisor = supervisors[num_students // 3 % num_supervisors]
#         remaining_group = {
#             'Supervisor': remaining_group_supervisor.username,
#             'Students': [student.user for student in remaining_group_students],
#             'Predictions': [student.prediction for student in remaining_group_students]
#         }
#         groups.append(remaining_group)

#     return groups

# record_groups = fetch_records()
# df = pd.DataFrame(record_groups)
# print(df)







# ##################################################################################################################
# import sqlite3
# import pandas as pd

# conn = sqlite3.connect('db.sqlite3')

# # Create a table in the database
# create_table_query = '''
#     CREATE TABLE IF NOT EXISTS new_project_group (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         supervisor TEXT,
#         student1 TEXT,
#         student2 TEXT,
#         student3 TEXT,
#         prediction TEXT
#     )
# '''
# conn.execute(create_table_query)
# num = 0
# for _, row in df.iterrows():
#     supervisor = row['Supervisor']
    
#     student1 = str(row['Students'][num])
    

#     try:
#         student2 = str(row['Students'][num+1])
#     except:student2 = ""
#     try:
#         student3 = str(row['Students'][num+2])
#     except:student3 = ''

#     predictions = ', '.join(row['Predictions'])

#     select_query = '''
#         SELECT COUNT(*) FROM new_project_group
#         WHERE supervisor = ? AND student1 = ? AND student2 = ? AND student3 = ? AND prediction = ? AND approved= ?
#     '''
    
#     try:
#         duplicate_check = conn.execute(select_query, (supervisor, student1, student2, student3, predictions, False)).fetchone()[0]
#     except:pass

#     if duplicate_check == 0:  
#         insert_query = '''
#             INSERT INTO new_project_group (supervisor, student1, student2, student3, prediction, approved)
#             VALUES (?, ?, ?, ?, ?, ?)
#         '''
#         conn.execute(insert_query, (supervisor, student1, student2, student3, predictions, False))
#         num += 3
#         print("Record inserted successfully.")

# conn.commit()
# conn.close()

###############################################################################################################

from django.shortcuts import render
from .models import NewProjectGroup

def edit_records(request):
    # Retrieve all existing records from the NewProjectGroup model
    records = NewProjectGroup.objects.all()

    context = {
        'records': records
    }
    
    return render(request, 'edit_records.html', context)






from django.shortcuts import render, redirect
from .forms import ProjectUploadForm
from .models import ProjectUploads

from django.shortcuts import render, redirect
from .forms import ProjectUploadForm
from .models import ProjectUploads

# def project_upload(request):
#     if request.method == 'POST':
#         form = ProjectUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             project_upload = form.save()
#             return redirect('home')
#     else:
#         form = ProjectUploadForm()
#     template = ['project_upload.html','home.html']
#     return render(request, template, {'form': form})


def project_upload(request):
    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the 'user' field to the current login username before saving
            if request.user.is_authenticated:
                form.instance.user = request.user.username
            project_upload = form.save()
            return redirect('home')
    else:
        # Set the 'user' field to the current login username in the initial data
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['user'] = request.user.username
        form = ProjectUploadForm(initial=initial_data)

    template = 'project_upload.html'
    return render(request, template, {'form': form})





################################################################################################################333

def project_list(request):
    project_uploads = ProjectUploads.objects.filter(project_stuff__supervisor=request.user)
    return render(request, 'project_list.html', {'project_uploads': project_uploads})


#################################################################
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ProjectUploads

# @login_required
# @user_passes_test(lambda user: user.groups.filter(name='DiagnosticAdmin').exists(), login_url='admin-login')
def project_approval(request, upload_id):
    upload = get_object_or_404(ProjectUploads, pk=upload_id)
    upload_docs = ProjectUploads.objects.all()
    if request.method == 'POST':
        upload.approved = True
        upload.save()
        return redirect('home')
        
    template = 'project_approval.html'
    context = {'upload': upload,
               'upload_docs':upload_docs,
               }
    return render(request, template, context)
