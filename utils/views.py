from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .utils import detect_gender, fix_persian_text

import pandas as pd
from django.shortcuts import render
from .forms import CSVUploadForm
from users.models import Buyer
from django.db.models import Q


from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, TicketCategory, TicketMessage
from .forms import TicketForm, TicketMessageForm
from django.contrib.auth.decorators import login_required



@login_required
def import_buyers_csv(request):
    created_count = 0
    updated_count = 0
    skipped_count = 0
    updated_names = []
    created_names = []
    skipped_names = []
    male_count = 0
    female_count = 0
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']

            col_first = request.POST.get('col_first')
            col_last = request.POST.get('col_last')
            col_phone = request.POST.get('col_phone')



            try:
                df = pd.read_csv(csv_file)
            except Exception as e:
                return render(request, 'import_csv.html', {
                    'form': form,
                    'error': 'خطا در خواندن فایل CSV: ' + str(e),
                })

            for _, row in df.iterrows():
                national_code = str(row.get('national_code', '')).strip()
                phone_number = str(row.get(col_phone, '')).strip()
                first_name = fix_persian_text(str(row.get(col_first, '')))
                last_name = fix_persian_text(str(row.get(col_last, '')))

                if  not phone_number :
                    skipped_count += 1
                    skipped_names.append(f'{first_name} {last_name}')
                    continue
                if  phone_number  == 'nan':
                    skipped_count += 1
                    skipped_names.append(f'{first_name} {last_name}')
                    continue
                

                if first_name == 'nan':
                    first_name = ''
                if last_name =='nan':
                    last_name = ''


                if last_name =='':
                    temp = first_name.split(' ')
                    if len(temp) > 1:
                        last_name = ' '.join(temp[1:])


                buyer = Buyer.objects.filter(first_name=first_name,last_name=last_name).first()

                if buyer:

                    buyer.phone_number = phone_number
                    buyer.save()
                    updated_count += 1
                    updated_names.append(f'{first_name} {last_name} {phone_number}')
                else:

                    # try:
                    buyer_created = False
                    if first_name !='':
                        gender = detect_gender(name=first_name)
                        if gender is not None:
                            gender = gender.lower()
                            if gender in ['male', 'female']:
                                Buyer.objects.create(
                                    first_name=first_name,
                                    last_name=last_name,
                                    phone_number=phone_number,
                                    gender = gender
                                )

                                if gender =='male':
                                    male_count+=1
                                else:
                                    female_count+=1

                                buyer_created = True

                    if not buyer_created:
                        Buyer.objects.create(
                            first_name=first_name,
                            last_name=last_name,
                            phone_number=phone_number,
                        )



                    created_count += 1
                    created_names.append(f'{first_name} {last_name} {phone_number}')


            return render(request, 'import_result.html', {
                'created': created_count,
                'updated': updated_count,
                'skipped': skipped_count,
                'created_names' : created_names,
                'update_names' : updated_names,
                'skipped_names' : skipped_names,
                'male_count':male_count,
                'female_count' : female_count,
                'not_detected' : abs(female_count-male_count),
            })
    else:
        form = CSVUploadForm()

    return render(request, 'import_csv.html', {'form': form})






from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, TicketCategory, TicketMessage
from .forms import TicketForm, TicketMessageForm
from django.contrib.auth.decorators import login_required


def ticket_list(request):
    user = request.user
    tickets = Ticket.objects.filter(
        Q(user=user) | Q(category__viewers=user)
    ).distinct().order_by('-created_at')
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})



@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        msg_form = TicketMessageForm(request.POST, request.FILES)
        if form.is_valid() and msg_form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            message = msg_form.save(commit=False)
            message.ticket = ticket
            message.sender = request.user
            message.save()
            return redirect('ticket_detail', ticket.id)
    else:
        categories = TicketCategory.objects.all()
        form = TicketForm()
        msg_form = TicketMessageForm()
        return render(request, 'tickets/ticket_create.html', {'form': form, 'msg_form': msg_form,'categories':categories})
    return redirect('error_page.html')
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    messages = ticket.messages.all().order_by('sent_at')
    if request.method == 'POST':

        if request.user != ticket.user and request.user not in ticket.category.viewers.all():
            return HttpResponseForbidden("شما اجازه مشاهده این تیکت را ندارید.")

        form = TicketMessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ticket = ticket
            msg.sender = request.user
            msg.save()
            return redirect('ticket_detail', ticket.id)
    else:
        form = TicketMessageForm()
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'messages': messages, 'form': form})
