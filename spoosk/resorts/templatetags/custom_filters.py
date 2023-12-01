from django import template
from resorts.models import SkiResort

register = template.Library()


@register.filter(name='string_formatting')  # регистрируем наш фильтр под именем
def string_formatting(value, arg):
    if arg == 1:
        value = f"Найден {arg} вариант:"
    elif 2 <= arg <= 4:
        value = f"Найдено {arg} варианта:"
    else:
        value = f"Найдено {arg} вариантов:"
    return value


def found_variants(num):
    if num == 1:
        return f"Найден {num} вариант:"
    elif 2 <= num <= 4:
        return f"Найдено {num} варианта:"
    else:
        return f"Найдено {num} вариантов:"


def format_results_count(n):
    word = ''
    if n == 1:
        word = 'вариант'
    elif n >= 2 and n <= 4:
        word = 'варианта'
    else:
        word = 'вариантов'
    return f'Найдено {n} {word}:'


# check if resort is in user's favorites
@register.filter(name='in_favorites')
def in_favorites(resort, user):
    if user.is_authenticated:
        if resort in SkiResort.objects.filter(users=user):
            return True
    else:
        return False

@register.filter
def create_range(value, start_index=0):
    return range(start_index, value+start_index)

@register.filter
def create_range_difference(value, end_index=5):
    return range(value, end_index)