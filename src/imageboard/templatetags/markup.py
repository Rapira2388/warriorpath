from django import template
from django.utils.safestring import mark_safe

from imageboard.wakabamark import parse_text


register = template.Library()


@register.simple_tag
def markup(text, board, thread, post, make_refs=True):

    rendered_text = parse_text(text, board, thread, post, make_refs)
    return mark_safe(rendered_text)
