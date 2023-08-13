from django import template

register = template.Library()

def multiply(value, arg):
    return value * arg




register.simple_tag(multiply)

from django import template

register = template.Library()

@register.filter
def count_words(value):
    # Split the value using comma as the delimiter and count the words
    return len(value.split(','))

# @register.simple_tag
# def display_project_upload(project_uploads, admin2_username, student):
#     for project_upload in project_uploads:
#         if project_upload.user == admin2_username or project_upload['user'] == student['Student1'] or project_upload['user'] == student['Student2'] or project_upload['user'] == student['Student3']:
#             return project_upload.description, project_upload.upload_file.url, project_upload.approved
#         return None, None, None