from django import template
from django.template.defaultfilters import stringfilter

from blog.utils.html_safety import safe_markdown_to_html

register = template.Library()


@register.filter
@stringfilter
def render_markdown(value):
    return safe_markdown_to_html(value)
