from django import template

register = template.Library()

@register.filter
def split_string(value, delimiter):
    return value.split(delimiter)[0].strip()



from django import template

register = template.Library()

@register.filter
def count_words(value):
    # Split the value using comma as the delimiter and count the words
    return len(value.split(','))
