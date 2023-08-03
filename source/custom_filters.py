from django import template

register = template.Library()

@register.filter
def split_string(value, delimiter):
    return value.split(delimiter)[0].strip()
