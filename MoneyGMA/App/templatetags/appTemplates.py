from django import template
import datetime

register = template.Library()

@register.filter
def prettyDate(value):
    date = datetime.datetime.strptime(value,"%Y-%m-%d")
    return date.strftime("%d %B %Y")