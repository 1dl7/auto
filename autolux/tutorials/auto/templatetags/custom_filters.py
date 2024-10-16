from django import template

register = template.Library()

@register.filter
def length_is(value, length):
    """Проверяет, равна ли длина объекта заданному значению."""
    return len(value) == int(length)
