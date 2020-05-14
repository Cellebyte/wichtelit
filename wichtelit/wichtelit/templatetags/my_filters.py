from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def comma(value: str) -> str:  # Only one argument.
    """Converts a string into all lowercase"""
    return value.replace('.', ',')
