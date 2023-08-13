from django.shortcuts import render
from .models import Room, Message
from diagnostic_centers.models import NewProjectGroup
import datetime 


from django.shortcuts import redirect
from .forms import MessageForm


def room(request):
    project_uploads = NewProjectGroup.objects.all()
    username = request.user.username
    pk_id = ""
    for project_upload in project_uploads:
        if project_upload.student1 == username:
            student_group = project_upload
            pk_id = f'{str(project_upload.prediction)}-{project_upload.pk}'

        elif project_upload.student2 == username:
            student_group = project_upload
            pk_id = f'{str(project_upload.prediction)}-{project_upload.pk}'

        elif project_upload.student3 == username:
            try:
                student_group = project_upload
                pk_id = f'{str(project_upload.prediction)}-{project_upload.pk}'
            except:pass
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # room = Room.objects.get(pk=1)
            forms = request.POST.get('message')
            message = Message(sender=request.user.username, content=forms, room=pk_id, timestamp=datetime.datetime.now())
            message.save()
            return redirect('chat_messages:room')
    else:
        form = MessageForm()
        username = request.user.username
        
        messages = Message.objects.all()
        try:
            pk_id2 = str(student_group.prediction).split(',')[0]
        except:pass
    context = {
        'form': form,
        'room' : student_group,
        'title' : pk_id2,
        'pk_id' : pk_id,
        'student_group' : project_uploads,
        'messages' : messages,
        'username' : request.user.username,
    }
    return render(request, 'chat_room.html', context)

from diagnostic_centers.models import DiagnosticAdmin

########################################################################


def supervisor_room2(request, supervisor_user=None):
    project_uploads = NewProjectGroup.objects.all()
    supervisor_user = str(supervisor_user)
    print("Username : ", supervisor_user)
    admin2 = Room.objects.filter(supervisor=supervisor_user)
    pk_id = ""
    for project_upload in project_uploads:
        if str(project_upload.supervisor).lower() == str(supervisor_user).lower():
            student_group = project_upload
            pk_id = project_upload.prediction
            pk = project_upload.id

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # room = Room.objects.get(pk=1)
            forms = request.POST.get('message')
            message = Message(sender=supervisor_user, content=forms, room=pk, timestamp=datetime.datetime.now())
            message.save()
            return redirect('chat_messages:supervisor_chat')
    else:
        form = MessageForm()
        
        messages = Message.objects.all()
        try:
            pk_id2 = str(pk_id).split(',')[0]
        except:pass
    context = {
        'form': form,
        # 'room' : student_group,
        'title' : pk_id2,
        'admin2' : admin2,
        'student_group' : project_uploads,
        'messages' : messages,
        'username' : supervisor_user,
    }
    return render(request, 'chat_room.html', context)


########################################################################




def supervisor_room(request, supervisor_user, room_id):
    project_uploads = NewProjectGroup.objects.filter(pk=room_id)
    supervisor_user = str(supervisor_user)
    print("Username : ", supervisor_user)
    admin2 = Room.objects.filter(supervisor=supervisor_user)
    pk_id = ""
    for project_upload in project_uploads:
        if str(project_upload.supervisor).lower() == str(supervisor_user).lower():
            student_group = project_upload
            pk_id = f'{str(project_upload.prediction)}-{project_upload.pk}'
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # room = Room.objects.get(pk=1)
            forms = request.POST.get('message')
            message = Message(sender=supervisor_user, content=forms, room=pk_id, timestamp=datetime.datetime.now())
            message.save()
            return redirect('chat_messages:supervisor_room', supervisor_user, room_id)
    else:
        form = MessageForm()
        
        messages = Message.objects.all()
        try:
            pk_id2 = str(pk_id).split(',')[0]
        except:pass
    context = {
        'form': form,
        # 'room' : student_group,
        'title' : pk_id2,
        'pk_id' : pk_id,
        'admin2' : admin2,
        'student_group' : project_uploads,
        'messages' : messages,
        'username' : supervisor_user,
    }
    return render(request, 'room.html', context)


