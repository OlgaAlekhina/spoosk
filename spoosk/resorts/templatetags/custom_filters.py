from django import template

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