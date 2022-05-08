from django import template

register = template.Library()

def get_count(dict, key):
    return dict[key]

def get_percent(num1, num2):
    try: 
        percent = (num1 / num2) * 100

        return round(percent, 2)
    
    except:
        return 0


register.filter('get_count', get_count)
register.filter('get_percent', get_percent)