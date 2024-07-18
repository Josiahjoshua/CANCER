from django import template

register = template.Library()

@register.filter
def percentage(value, total):
    if total == 0:
        return 0
    return (value / total) * 100

def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0.0