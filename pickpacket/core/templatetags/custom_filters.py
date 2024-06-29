from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    try:
        return abs(float(value) - float(arg))
    except (ValueError, TypeError):
        return ''

@register.filter
def percentage_decrease(original, optimized):
    try:
        original = float(original)
        optimized = float(optimized)
        decrease = abs(original - optimized)
        percentage = (decrease / original) * 100
        return round(percentage, 2)
    except (ValueError, TypeError):
        return ''
