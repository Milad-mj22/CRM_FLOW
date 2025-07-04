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
