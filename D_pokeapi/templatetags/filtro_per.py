from django import template

register = template.Library()

@register.filter
def range(valor, saltos):
    try:
        rango = range(0, int(valor), int(saltos))
        return rango
    except(ValueError, TypeError):
        return range(0)