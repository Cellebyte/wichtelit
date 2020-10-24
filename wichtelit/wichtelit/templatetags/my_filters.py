from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def comma(value: str) -> str:  # Only one argument.
    """Converts a string into all lowercase"""
    value = f'{float(value):.2f}'
    return value.replace('.', ',')
