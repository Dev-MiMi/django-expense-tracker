from django import template

register = template.Library()

@register.filter
def divided_by(value, divisor):
    try:
        return (float(value) / float(divisor)) * 100
    except (ValueError, ZeroDivisionError):
        return 0
