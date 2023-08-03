from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.views.decorators.csrf import csrf_exempt
from sklearn.mixture import GaussianMixture
import pandas as pd
import numpy as np
from diagnostic_centers.models import Groups, Students
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from diagnostic_centers.models import DiagnosticAdmin, Students
from .forms import AdminLoginForm, StaffLoginForm
from django.http import JsonResponse
from .models import Message
import sqlite3
import pandas as pd
from diagnostic_centers.models import ProjectUploads
from diagnostic_centers.models import Questionnaire

def home(request):
    def fetch_records():
        supervisors = list(DiagnosticAdmin.objects.all())
        students = list(Questionnaire.objects.all().order_by('prediction'))
        num_students = len(students)
        num_supervisors = len(supervisors)
        groups = []

        for i in range(0, num_students, 3):
            group_students = students[i:i + 3]
            group_supervisor = supervisors[i // 3 % num_supervisors]
            group = {
                'Supervisor': group_supervisor.username,
                'Students': [student.user for student in group_students],
                'Predictions': [student.prediction for student in group_students]
            }
            groups.append(group)

        # Handle remaining students
        remaining_students = num_students % 3
        if remaining_students:
            remaining_group_students = students[-remaining_students:]
            remaining_group_supervisor = supervisors[num_students // 3 % num_supervisors]
            remaining_group = {
                'Supervisor': remaining_group_supervisor.username,
                'Students': [student.user for student in remaining_group_students],
                'Predictions': [student.prediction for student in remaining_group_students]
            }
            groups.append(remaining_group)

        return groups

    
    record_groups = fetch_records()
    df = pd.DataFrame(record_groups)
    userid = request.user.id
    questions = Questionnaire.objects.filter(user_id=userid)
    
    project_uploads = ProjectUploads.objects.all()
   
    username = request.user.username
    num = 0
    student = dict()
    for _, row in df.iterrows():
        supervisor = row['Supervisor']
        title = row["Predictions"]
        student1 = str(row['Students'][num])
        

        try:
            student2 = str(row['Students'][num+1])
        except:student2 = ""
        try:
            student3 = str(row['Students'][num+2])
        except:student3 = ''

        if str(student1) == str(username):
            student.update(
                {
                    'Supervisor' : supervisor,
                    'Student1' : username,
                    'Student2' : student2,
                    'Student3' : student3,
                    'Title' : title[0],
                }
            )
        elif str(student2) == str(username):
            student.update(
                {
                    'Supervisor' : supervisor,
                    'Student1' : student1,
                    'Student2' : username,
                    'Student3' : student3,
                    'Title' : title[0],
                }
            )
        elif str(student3) == str(username):
            student.update(
                {
                    'Supervisor' : supervisor,
                    'Student1' : student1,
                    'Student2' : student2,
                    'Student3' : username,
                    'Title' : title[0],
                }
            )
        else:
            pass
            # print("------------------------")
    template = 'home.html'
    groups = Groups.objects.all()
    prediction = ""
    

    context = {'groups': groups,
               'username' : username,
               'project_uploads':project_uploads,
               'questions':questions,
               'student': student,
               }
    return render(request, template, context)


def staff_logout(request):
    #messages.success(request, 'Logged Out.', extra_tags='html_safe')
    return redirect('diagnostic_centers:staff-login')


def admin_login(request):
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

def admin_dashboard(request):
    template = 'diagnostic_centers/admin_dashboard.html'
    groups = Groups.objects.all()
    admin = DiagnosticAdmin.objects.all()
    context = { 'groups': groups,
               'admin':admin,
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
    groups = Groups.objects.all()
    print(groups)
    context = {
        'staff': staff,
        'admins': admins,
        'staff_username': username, 
           'groups': groups,
              }
    return render(request, template, context)

def staff_logout(request):
    # messages.success(request, 'Logged Out.', extra_tags='html_safe')
    return redirect('diagnostic_centers:staff-login')

def center_details(request, id=id):
    template = 'diagnostic_centers/center_details.html'
    return render(request, template)


#####################################################################################################################

@login_required
def q(request):
    if request.user.is_authenticated:
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
    else:
        return render(request,'home.html')

from .forms import MessageForm
def chat(request):
    form = MessageForm()
    if request.method == "POST":
        forms = request.POST.get('message')
        print(forms)
    messages = Message.objects.all()
    message = Message(sender=request.user, content=forms)
    message.save()
    print("Saved Successfully")
    return render(request, 'chat.html', {'form': form, 'messages': messages})

def supervisor_chat(request):
    form = MessageForm()
    forms = ''
    if request.method == "POST":
        forms = request.POST.get('message')
        print(forms)
    messages = Message.objects.all()
    message = Message(sender=request.user, content=forms)
    message.save()
    print("Saved Successfully")
    userid = request.user.id
    questions = Questionnaire.objects.filter(user_id=userid)
    project_uploads = ProjectUploads.objects.all()
    username = request.user
    username1 = request.user.username
    print(username)
    conn = sqlite3.connect('db.sqlite3')
    query = "SELECT * FROM new_project_group"
    fdf = pd.read_sql_query(query, conn)
    df = fdf[fdf.apply(lambda row: username1 in ' '.join(row.values.astype(str)), axis=1)]
    groups = Groups.objects.all()
    prediction = df["prediction"]
    prediction = str(prediction).split(',')
    prediction = prediction[0]
    prediction = prediction.replace('5','')
    return render(request, 'supervisor_chat.html', {'form': form, 'messages': messages, 'group':prediction, 'user' : username})
           

    


def load_messages(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        data = [{'content': message.content, 'sender': message.sender.username} for message in messages]
        return JsonResponse(data, safe=False)
    return JsonResponse({}, status=400)
