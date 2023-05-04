from django import template

register = template.Library()

def string_kr(value):
    if value == 'traditional':
        return '전통주'
    elif value == 'beer':
        return '맥주'
    elif value == 'whiskey':
        return '위스키'
    elif value == 'wine':
        return '와인'
    elif value == 'low':
        return '약한'
    elif value == 'middle':
        return '중간'
    elif value == 'strong':
        return '강한'
    elif value == 'True':
        return '있음'
    elif value == 'False':
        return '없음'
    elif value == 'man':
        return '남'
    elif value == 'woman':
        return '여'

register.filter('string_kr',string_kr)

