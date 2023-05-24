from django import template

register = template.Library()


@register.simple_tag()
def get_price_with_sale(price, sale: int):
    price = str(int(price - price / 100 * sale))
    done_str = ''
    count_symbols = 0
    for i in range(len(price) - 1, -1, -1):
        if count_symbols < 3:
            done_str += price[i]
            count_symbols += 1
        else:
            done_str += ' '
            done_str += price[i]
            count_symbols = 1
    return done_str[::-1]


@register.simple_tag()
def get_int_price(price):
    price = str(int(price))
    done_str = ''
    count_symbols = 0
    for i in range(len(price) - 1, -1, -1):
        if count_symbols < 3:
            done_str += price[i]
            count_symbols += 1
        else:
            done_str += ' '
            done_str += price[i]
            count_symbols = 1
    return done_str[::-1]


@register.filter()
def rangeOn(num=2):
    return range(num)


@register.filter()
def rangeOnCountGrayStar(num=2):
    return range(5 - num)
