from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CoopAttribute, CoopAttributeValue
from django.http import HttpResponseForbidden
from StoneFlow.models import coops
from mines.models import Mine
from users.models import Profile, mother_material , raw_material
# Create your views here.
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from decimal import Decimal
from django.core.files.base import ContentFile
import base64
from django.db.models import Q


from .models import Driver, coops, STATE_CHOICES
# views.py
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


def get_allowed_confirm_users(stepNumber:int):

    if stepNumber==1:
        allowed_roles = ['manager', 'fishzan','Programmer','Driver']  # Adjust based on your logic
        return allowed_roles

    if stepNumber==2:
        allowed_roles = ['manager', 'fishzan']  # Adjust based on your logic
        return allowed_roles

    if stepNumber==3:
        allowed_roles = ['manager', 'fishzan','Programmer']  # Adjust based on your logic
        return allowed_roles
  
    if stepNumber==4:
        allowed_roles = ['manager', 'fishzan']  # Adjust based on your logic
        return allowed_roles  

def convertName2Step(self,name):
    if name =='create_coope':
        return 1


def get_submit_and_confirmed(user,stepNumber):
        user_profile = Profile.objects.get(user=user)
        user_role = user_profile.job_position.name
        allowed_roles = get_allowed_confirm_users(stepNumber=1)
        # Check if the user has access to submit this step
        can_submit = user_role in allowed_roles
        # is_confirmed = check_order_confirmed(order=ret,stepNumber=1)
        is_confirmed = False
        return can_submit , is_confirmed







def coops_by_state(request):
    selected_state = request.GET.get('state')
    selected_material_id = request.GET.get('material')
    page = int(request.GET.get('page', 1))

    coop_list = coops.objects.all().order_by('-id')
    steps = Step.objects.order_by('order')  # مرتب‌سازی مراحل
    materials = raw_material.objects.all()

    if selected_state:
        coop_list = coop_list.filter(state=selected_state)
    if selected_material_id:
        coop_list = coop_list.filter(material_id=selected_material_id)

    paginator = Paginator(coop_list, 10)
    page_obj = paginator.get_page(page)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/coop_cards.html', {'coops': page_obj})
        return JsonResponse({'html': html, 'has_next': page_obj.has_next(), 'next_page': page + 1})

    context = {
        'coops': page_obj,
        'steps': steps,
        'selected_state': selected_state,
        'materials': materials,
        'selected_material_id': selected_material_id,
    }
    return render(request, 'coop_list.html', context)

def coop_detail(request, coop_id):
    coop = get_object_or_404(coops, id=coop_id)

    user_access_qs = StepAccess.objects.filter(user=request.user)
    step_access = {access.step.id: access.access_level for access in user_access_qs}


    return render(request, 'coop_detail.html', {'coop': coop,'step_access':step_access})








def coop_dashboard(request):
    material_id = request.GET.get('material_id')
    materials = raw_material.objects.all()
    selected_material = None
    qs = coops.objects.all()

    if material_id:
        qs = qs.filter(material_id=material_id)
        selected_material = raw_material.objects.filter(id=material_id).first()

    # آماده‌سازی داده برای چارت‌ها
    state_counts = {}
    for state_code, state_name in coops._meta.get_field('state').choices:
        state_counts[state_name] = qs.filter(state=state_code).count()

    chart_labels = list(state_counts.keys())
    chart_data = list(state_counts.values())

    return render(request, 'coop_dashboard.html', {
        'materials': materials,
        'selected_material': selected_material,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })


from django.db import transaction
@login_required
@transaction.atomic
def create_coope(request):
    stepNumber = 1

    if request.method == 'POST':
        coop_record = None  # در سطح بالا تعریف می‌کنیم که در except هم قابل دسترسی باشد
    # try:
        data = dict(request.POST.dict())
        data.pop('csrfmiddlewaretoken', None)

        image = None
        image_data = request.POST.get('image_data')
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr), name='captured_image.' + ext)
            data.pop('image_data', None)

        mine_id = request.POST.get('mine_id')
        if not mine_id:
            messages.error(request, "لطفاً یک معدن انتخاب کنید.")
            raise Exception("معدن انتخاب نشده")

        selected_mine = Mine.objects.filter(id=mine_id).first()
        if not selected_mine:
            messages.error(request, "معدن انتخاب‌شده یافت نشد.")
            raise Exception("معدن نامعتبر")

        # ذخیره وزن‌ها
        full_weight = request.POST.get('full_weight')
        empty_weight = request.POST.get('empty_weight')
        net_weight = request.POST.get('net_weight')

        data.pop('full_weight', None)
        data.pop('empty_weight', None)
        data.pop('net_weight', None)
        data.pop('mine_id', None)

        step = Step.objects.filter(order = 1).first()

        # ثبت مواد خام
        for field, value in data.items():
            try:
                if value and float(value) > 0:
                    raw_material_obj = raw_material.objects.get(name=field)
                    coop_record = coops.objects.create(
                        user=request.user,
                        material=raw_material_obj,
                        quantity=Decimal(value),
                        state = step,
                        image=image
                    )
            except Exception as e:
                # raise Exception(f"خطا در ثبت مواد اولیه: {field}")
                print('Error is Save Raw amterial', field)

        if coop_record is None:
            raise Exception("هیچ کوپی ثبت نشد")

        # ثبت ویژگی‌های دینامیک
        attributes = CoopAttribute.objects.filter(step=stepNumber)
        for attr in attributes:
            field_name = f'attr_{attr.id}'
            value = request.POST.get(field_name, '').strip()

            if attr.required and not value:
                messages.error(request, f'فیلد "{attr.label}" الزامی است.', extra_tags='create_coop_error')
                raise Exception(f'فیلد الزامی "{attr.label}" خالی است')

            if value:
                CoopAttributeValue.objects.create(
                    coop=coop_record,
                    attribute=attr,
                    value=value
                )

        messages.success(request, "مقادیر با موفقیت ثبت شدند.")
        return render(request, 'success_page.html', {'content': 'حواله جدید با موفقیت ثبت گردید'})

        # except Exception as e:
        #     print('❌ خطا در ثبت اطلاعات:', e)

        #     # اگر کوپ ساخته شده، آن را حذف کن
        #     if coop_record:
        #         coop_record.delete()

        #     messages.error(request, 'خطا در ذخیره اطلاعات. تمام داده‌ها حذف شدند.')
        #     return redirect(request.path)

    else:
        # GET
        attributes = CoopAttribute.objects.filter(step=stepNumber)
        can_submit, is_confirmed = get_submit_and_confirmed(user=request.user, stepNumber=stepNumber)
        mother_materials = mother_material.objects.prefetch_related('mother_material').order_by('describe').all()
        mines = Mine.objects.all()


        steps = Step.objects.order_by('order')  # مرتب‌سازی مراحل


        return render(request, 'stone_section1.html', {
            'mother_materials': mother_materials,
            'is_confirmed': is_confirmed,
            'can_submit': can_submit,
            'mines': mines,
            'attributes': attributes,  # 👈 ارسال ویژگی‌ها به قالب
            'steps': steps,
        })




# def coop_state_detail(request, coop_id, state):

#     if state==STATE_CHOICES[0][0]:
#         ret = create_coope(request=request)
#         return ret

#     # coop = get_object_or_404(coops, id=coop_id)
#     # history = coop.state_history.filter(new_state=state).last()
#     # return render(request, 'coop/coop_state_detail.html', {
#     #     'coop': coop,
#     #     'state': state,
#     #     'history': history,
#     # })




from django.shortcuts import render, get_object_or_404, redirect
from .models import Step, coops, CoopStateHistory  # فرضی
from django.http import Http404

def coop_state_detail(request, coop_id, state):
    try:
        step = Step.objects.get(url_name=state)
    except Step.DoesNotExist:
        return render(request, 'step_not_found.html', {
            'state': state,
            'coop_id': coop_id
        })

    if step.url_name == 'create_coope':
        return create_coope(request=request)

    coop = get_object_or_404(coops, id=coop_id)

    # ویژگی‌های مربوط به این مرحله
    attributes = CoopAttribute.objects.filter(step=step)

    # مقادیر ذخیره‌شده مربوط به این کوپ و این ویژگی‌ها
    attribute_values = {
        av.attribute_id: av.value
        for av in coop.attribute_values.filter(attribute__in=attributes)
    }

    history = coop.state_history.filter(new_state=state).last()

    return render(request, 'coop_state_detail.html', {
        'coop': coop,
        'state': state,
        'history': history,
        'step': step,
        'attributes': attributes,
        'attribute_values': attribute_values
    })









def dynamic_step_view(request, url_name, order_id=None):
    try:
        step = Step.objects.get(url_name=url_name)
        # اینجا می‌تونی بر اساس نوع step اقدام خاصی انجام بدی
        return render(request, 'step_placeholder.html', {
            'step': step,
            'order_id': order_id,
        })
    except Step.DoesNotExist:
        return render(request, 'step_not_found.html', {
            'url_name': url_name
        })









# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CoopAttributeForm, DriverRegisterForm, StepForm

from users.models import jobs,User,Profile
from django.db import transaction



def driver_list_view(request):
    drivers = Driver.objects.all()
    return render(request, 'drivers/driver_list.html', {'drivers': drivers})



def register_driver(request):
    if request.method == 'POST':
        form = DriverRegisterForm(request.POST)
        if form.is_valid():
            try:
                # ایجاد تراکنش امن
                with transaction.atomic():
                    # ایجاد کاربر
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                    )

                    # # دریافت موقعیت شغلی "راننده"
                    # try:
                    #     driver_job = jobs.objects.get(persian_name="راننده")
                    # except jobs.DoesNotExist:
                    #     messages.error(request, "شغل 'راننده' در سیستم تعریف نشده است. لطفاً با مدیر تماس بگیرید.")
                    #     user.delete()  # حذف کاربر
                    #     return render(request, 'drivers/register_driver.html', {'form': form})

                    # ساخت پروفایل


                    # 1. گرفتن پروفایل مربوط به آن کاربر:
                    profile = get_object_or_404(Profile, user=user)

                    # 2. مقدار جدید برای job_position (مثلاً راننده):
                    driver_job = get_object_or_404(jobs, persian_name="راننده")

                    # 3. آپدیت مقدار
                    profile.job_position = driver_job
                    profile.first_name = form.cleaned_data['first_name']
                    profile.last_name = form.cleaned_data['last_name']

                    # 4. ذخیره تغییرات
                    profile.save()




                    # ساخت شیء راننده
                    driver = form.save(commit=False)
                    driver.user = user
                    driver.save()

                    messages.success(request, "ثبت‌نام راننده با موفقیت انجام شد.")
                    return redirect('login')

            except Exception as e:
                # در صورت خطا در هر مرحله، کاربر و پروفایل حذف شود
                if 'user' in locals():
                    user.delete()
                messages.error(request, f"خطا در ثبت‌نام: {str(e)}")
                return render(request, 'drivers/register_driver.html', {'form': form})

    else:
        form = DriverRegisterForm()
    
    return render(request, 'drivers/register_driver.html', {'form': form})



from .forms import DriverRegisterForm
from django.contrib import messages

def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    if request.method == 'POST':
        form = DriverRegisterForm(request.POST, instance=driver)
        if form.is_valid():
            form_instance = form.save(commit=False)
            # به‌روزرسانی اطلاعات کاربر
            user = driver.user
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            form_instance.save()
            return redirect('driver_list')
    else:
        initial = {
            'username': driver.user.username,
            'first_name': driver.user.first_name,
            'last_name': driver.user.last_name,
        }
        form = DriverRegisterForm(instance=driver, initial=initial)

    return render(request, 'drivers/edit_driver.html', {'form': form})



def delete_driver_view(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)

    if request.method == 'POST':
        user = driver.user
        driver.delete()
        user.delete()  # حذف یوزر مرتبط
        messages.success(request, "راننده با موفقیت حذف شد.")
        return redirect('driver_list')

    return render(request, 'drivers/delete_confirm.html', {'driver': driver})





from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def manage_coop_attributes(request):
    form = CoopAttributeForm()
    attributes = CoopAttribute.objects.all()

    if request.method == 'POST':
        if 'edit_id' in request.POST:
            attr = get_object_or_404(CoopAttribute, id=request.POST['edit_id'])
            form = CoopAttributeForm(request.POST, instance=attr)
            if form.is_valid():
                form.save()
                messages.success(request, 'ویژگی با موفقیت ویرایش شد.', extra_tags='create_coop_feature_success')
                return redirect('manage_coop_attributes')
        elif 'delete_id' in request.POST:
            attr = get_object_or_404(CoopAttribute, id=request.POST['delete_id'])
            attr.delete()
            messages.success(request, 'ویژگی حذف شد.', extra_tags='create_coop_feature_success')
            return redirect('manage_coop_attributes')
        else:
            form = CoopAttributeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'ویژگی جدید اضافه شد.', extra_tags='create_coop_feature_success')
                return redirect('manage_coop_attributes')
            else:
                # Print errors to console (terminal) for debugging
                print(form.errors)
                messages.error(request, ' نام ویژگی تکراری است یا فرم کامل پرنشده است.', extra_tags='create_coop_feature_error')

    return render(request, 'manage_attributes.html', {
        'form': form,
        'attributes': attributes
    })





from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Step, StepAccess

def manage_access(request):
    # users = User.objects.all()
    # steps = Step.objects.all()

    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )
    else:
        users = User.objects.all()

    steps = Step.objects.all()



    if request.method == 'POST':
        # Receive data from form: 
        # expect keys like access_USERID_STEPID = 'view' or 'submit' or ''(no access)
        for user in users:
            for step in steps:
                key = f'access_{user.id}_{step.id}'
                level = request.POST.get(key, '')
                # Update or delete StepAccess accordingly
                if level in ['view', 'submit']:
                    obj, created = StepAccess.objects.update_or_create(
                        user=user, step=step,
                        defaults={'access_level': level}
                    )
                else:
                    StepAccess.objects.filter(user=user, step=step).delete()
        return redirect('manage_access')  # redirect to refresh page

    # Prepare current access matrix
    access_matrix = {}
    for user in users:
        access_matrix[user.id] = {}
        for step in steps:
            try:
                sa = StepAccess.objects.get(user=user, step=step)
                access_matrix[user.id][step.id] = sa.access_level
            except StepAccess.DoesNotExist:
                access_matrix[user.id][step.id] = ''

    context = {
        'users': users,
        'steps': steps,
        'access_matrix': access_matrix,
    }
    return render(request, 'manage_access.html', context)





def steps_list(request):
    steps = Step.objects.order_by('order')
    return render(request, 'steps_list.html', {'steps': steps})


def manage_step(request, step_id=None):
    if step_id:
        step = get_object_or_404(Step, id=step_id)
    else:
        step = None

    form = StepForm(request.POST or None, instance=step)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('steps_list')  # آدرس لیست مراحل

    return render(request, 'manage_step.html', {
        'form': form,
        'is_edit': step is not None
    })



def delete_step(request, step_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("اجازه دسترسی ندارید.")

    step = get_object_or_404(Step, id=step_id)
    step.delete()
    messages.success(request, "مرحله با موفقیت حذف شد.")
    return redirect('steps_list')