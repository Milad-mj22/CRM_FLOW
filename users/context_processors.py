
from users.models import MenuItem, UserRole



def menu_items_processor(request):
    user = request.user
    if not user.is_authenticated:
        return {'menu_items': []}

    # گرفتن نقش‌های کاربر
    roles = UserRole.objects.filter(user=user).values_list('role_id', flat=True)

    # گرفتن آیتم‌های منو مرتبط با نقش‌ها
    items = MenuItem.objects.filter(roles__id__in=roles).distinct().order_by('order')

    return {'menu_items': items}