from django import template

register = template.Library()

@register.filter
def has_approved_project(project_uploads, user):
    flag = False
    for project_upload in project_uploads:
        if project_upload.user == user:
            flag = True
            break
    return flag

@register.filter 
def has_approved_project2(project_uploads, student):
    flag = False
    for index in student:
        for project_upload in project_uploads:
            if project_upload.user == student['Student1'] or project_upload.user == student['Student2'] or project_upload.user == student['Student3']:
                if project_upload.approved:
                    flag = True
                    break
    return flag
            