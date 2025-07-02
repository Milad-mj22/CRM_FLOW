from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from StoneFlow.models import coops
from users.models import Profile, mother_material , raw_material
# Create your views here.
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from decimal import Decimal
from django.core.files.base import ContentFile
import base64


from .models import coops, STATE_CHOICES
# views.py
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


def get_allowed_confirm_users(stepNumber:int):

    if stepNumber==1:
        allowed_roles = ['manager', 'fishzan','Programmer']  # Adjust based on your logic
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
        'states': STATE_CHOICES,
        'selected_state': selected_state,
        'materials': materials,
        'selected_material_id': selected_material_id,
    }
    return render(request, 'coop_list.html', context)

def coop_detail(request, coop_id):
    coop = get_object_or_404(coops, id=coop_id)
    return render(request, 'coop_detail.html', {'coop': coop})








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




@login_required
def create_coope(request):
    stepNumber=1

    if request.method == 'POST':
        try:
            
            data = dict(request.POST.dict())
            data.pop('csrfmiddlewaretoken','Not found')

            materials_data = []

            image = None

            if 'image_data' in data.keys():
                image_data = request.POST.get('image_data')
                data.pop('image_data','Not found')

            else:
                return
            

            if 'full_weight' in data.keys() and 'empty_weight' in data.keys() and 'net_weight' in data.keys():

                full_weight = request.POST.get('full_weight')
                data.pop('full_weight','Not found')

                empty_weight = request.POST.get('empty_weight')
                data.pop('empty_weight','Not found')

                net_weight = request.POST.get('net_weight')
                data.pop('net_weight','Not found')


                print('full_weight : ',full_weight,'  empty_weight : ',empty_weight,'  net_weight : ',net_weight)

            else:
                return

            
            if image_data:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                image = ContentFile(base64.b64decode(imgstr), name='captured_image.' + ext)



            # for name, quantity in zip(materials_names, materials_sent):
            #     try:
            #         quantity_value = float(quantity) if quantity else 0
            #     except ValueError:
            #         quantity_value = 0  # fallback in case of invalid input




            #     materials_data.append({
            #         'name': name,
            #         'sent_quantity': quantity_value
            #     })

            #     raw_material_obj = raw_material.objects.filter(name=name).first()

            #     coops.objects.create(
            #         user=request.user,
            #         material=raw_material_obj,
            #         quantity=Decimal(quantity_value),
            #         image = image
            #     )

            values ={}
            for field,value in data.items():
                # try:
                    if value !='':
                        if float(value)>0:
                            values[field]=value


                            raw_material_obj = raw_material.objects.get(name=field)
                            coops.objects.create(
                                user=request.user,
                                material=raw_material_obj,
                                quantity=Decimal(value),
                                image = image
                            )

                # except:
                #     print('error in add to coops')
                #     messages.success(request,'بروز خطا در هنگام اضافه نمودن کوپ')
                #     return redirect('/')  # Redirect to your desired page



            # 👉 process/save data here
            print(materials_data)  # For debugging

            # Optionally redirect or add message
            messages.success(request, "مقادیر با موفقیت ثبت شدند.")
            return render(request=request,template_name='success_page.html',context={'content':'حواله جدید با موفقیت ثبت گردید'})
            
        
        except:
            messages.error(request,'خطا در ذخیره اطلاعات')
            return redirect("")  # هدایت به صفحه دیگر


    else:


        context = {
            'order_id': 1,
        }

        can_submit , is_confirmed = get_submit_and_confirmed(user=request.user,stepNumber=stepNumber)

        raw_materials_obj = raw_material.objects.all()

        mother_materials = mother_material.objects.prefetch_related('mother_material').order_by('describe').all()


        return render(request, 'stone_section1.html',{
                    #   'material_usages':raw_materials_obj,
                    'mother_materials':mother_materials,

                      'is_confirmed':is_confirmed,
                      'can_submit':can_submit
                      })






def coop_state_detail(request, coop_id, state):

    if state==STATE_CHOICES[0][0]:
        ret = create_coope(request=request)
        return ret

    # coop = get_object_or_404(coops, id=coop_id)
    # history = coop.state_history.filter(new_state=state).last()
    # return render(request, 'coop/coop_state_detail.html', {
    #     'coop': coop,
    #     'state': state,
    #     'history': history,
    # })




# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DriverRegisterForm

from users.models import jobs,User,Profile

def register_driver(request):
    if request.method == 'POST':
        form = DriverRegisterForm(request.POST)
        if form.is_valid():
            # ساخت یوزر
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            # یافتن شغل "راننده"
            driver_job = jobs.objects.get(name="راننده")  # یا هر فیلدی که داری مثل code='driver'

            # ساخت پروفایل با موقعیت شغلی راننده
            Profile.objects.create(
                user=user,
                first_name=form.cleaned_data.get('full_name', '').split(' ')[0],
                last_name=form.cleaned_data.get('full_name', '').split(' ')[-1],
                job_position=driver_job
            )

            # ساخت شیء Driver
            driver = form.save(commit=False)
            driver.user = user
            driver.save()

            messages.success(request, "راننده با موفقیت ثبت شد.")
            return redirect('login')
    else:
        form = DriverRegisterForm()
    return render(request, 'drivers/register_driver.html', {'form': form})
