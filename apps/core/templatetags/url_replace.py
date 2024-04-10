# https://stackoverflow.com/questions/2047622/how-to-paginate-django-with-other-get-variables/62587351#62587351
from urllib.parse import urlencode
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.pop('page', None)
    query.update(kwargs)
    return query.urlencode()