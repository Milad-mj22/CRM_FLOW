from django import template

register = template.Library()


@register.filter
def split_license(plate):
    if not plate:
        return ['--', '--', '---', '--']

    if isinstance(plate, list):
        # اگر لیست است (مثلاً هنگام نمایش فرم با خطا)، همان لیست را برگردان
        return plate

    try:
        parts = plate.split('-')
        if len(parts) == 4:
            return parts
    except Exception:
        pass

    return ['--', '--', '---', '--']



from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    if not value:
        return []
    # اگر بخوای فقط یک جداکننده باشه (مثلاً کامای فارسی)
    if delimiter == ',':
        # جدا کردن هم با کامای انگلیسی و هم فارسی
        import re
        return [item.strip() for item in re.split(r'[،,]', value)]
    else:
        return [item.strip() for item in value.split(delimiter)]



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')