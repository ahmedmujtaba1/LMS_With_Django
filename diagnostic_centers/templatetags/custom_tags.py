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
