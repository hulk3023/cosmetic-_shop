from django import template

register = template.Library()

# Oddiy filtr: ko'paytirish
@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''